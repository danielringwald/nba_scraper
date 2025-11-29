from time import sleep
import duckdb
import pandas as pd
import regex as re
import logging
import argparse

from nba_api.stats.library.data import teams as NBA_TEAMS
from nba_api.stats.endpoints import scheduleleaguev2
from nba_api.stats.endpoints import boxscoretraditionalv3

from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
# TODO add PlayerCareerStatsRepository (has all the PTS per games, etc.)
from nba_scraper.configuration.database_config import TEAM_NAME_INFORMATION_TABLE_NAME
from nba_scraper.configuration.logging_config import init_logging
from nba_scraper.utils import Utils

init_logging()
logger = logging.getLogger(__name__)

RATE_LIMIT_SLEEP_SECONDS = 1


class PopulateDatabase:

    def __init__(self, con: duckdb.DuckDBPyConnection):
        self.con = con
        self.sgd = SeasonGamesRepository()
        self.bstr = BoxScoreTraditionalRepository()

    def populate_all_databases(self, season: str = "2024-25"):
        logger.info("Starting database population for season %s", season)
        self.populate_teams_information_datebase()
        self.populate_season_games_datebase(
            season=season, exclude_game_labels=["Preseason"])

        tries = 3
        for attempt in range(tries):
            try:
                self.populate_box_score_datebase(
                    season=season)
                break
            except ValueError as e:
                logger.warning(
                    "Attempt %s of %s failed with error: %s", attempt + 1, tries, e)
                if attempt < tries - 1:
                    logger.warning("Retrying...")
                    sleep(5)
                else:
                    logger.error("All attempts failed.")

    def populate_teams_information_datebase(self):
        table_name = TEAM_NAME_INFORMATION_TABLE_NAME

        exists = self.con.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?
        """, [table_name]).fetchone()[0] > 0

        if exists:
            number_of_rows = self.con.execute(
                f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

            if number_of_rows == 30:
                print(
                    f"Table {table_name} already populated with 30 teams, skipping population.")
                return

        self.perform_create_teams_information_table(table_name=table_name)

        # This is a list with the following information as taken from nba_api.stats.library.data.md from nba_api
        # team_id, abbreviation, nickname, year_founded, city, full_name, state
        for team in NBA_TEAMS:
            team_id = team[0]
            team_abbreviation = team[1]
            team_name = team[5]

            df = pd.DataFrame(
                {
                    "team_id": [team_id],
                    "team_abbreviation": [team_abbreviation],
                    "team_name": [team_name]
                })

            self.con.register("dataframe_to_insert", df)
            self.con.execute(
                f"INSERT INTO {table_name} SELECT * FROM dataframe_to_insert")
            logger.info("Inserted team: %s", team_name)

    def perform_create_teams_information_table(self, table_name: str):
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                team_id TEXT PRIMARY KEY,
                team_abbreviation TEXT,
                team_name TEXT
            )
            """)
        logger.info("Table %s created successfully", table_name)

    # Games Schedule

    def populate_season_games_datebase(self, season: str = "2024-25", exclude_game_labels: list[str] = None):
        if exclude_game_labels is None:
            exclude_game_labels = []

        if not re.match(r'^\d{4}-\d{2}$', season):
            raise ValueError(
                "Invalid season format. Must be in the format 'YYYY-YY', e.g., '2023-24'.")

        table_name = "season_games"

        self.perform_create_season_games_table(table_name=table_name)

        data = scheduleleaguev2.ScheduleLeagueV2(season=season)

        # Reference: https://github.com/swar/nba_api/blob/1539c400d8f7a4f588e11a2f3e95ca1e4a74ab0f/docs/nba_api/stats/endpoints/scheduleleaguev2.md
        season_games: pd.DataFrame = data.get_data_frames()[0]

        if not isinstance(season_games, pd.DataFrame):
            raise ValueError(
                "Expected a pandas DataFrame from ScheduleLeagueV2 from the NBA API response.")

        season_games_subset = season_games[[
            "gameId",
            "seasonYear",
            "gameDate",
            "gameStatus",
            "gameLabel",
            "homeTeam_teamId",
            "homeTeam_teamTricode",  # They call it tricode, I call it abbreviation
            "homeTeam_score",
            "awayTeam_teamId",
            "awayTeam_teamTricode",
            "awayTeam_score"
        ]]
        season_games_subset.loc[:, "gameDate"] = pd.to_datetime(
            season_games_subset["gameDate"]).dt.date

        # Add to exclude_game_labels list which values of game_label that should be filtered out
        # This way one can exclude preseason games or playoff, for example
        for excluded_game_label in exclude_game_labels:
            season_games_subset = season_games_subset[
                season_games_subset["gameLabel"] != excluded_game_label
            ]

        # Filter out future games
        season_games_subset = season_games_subset[
            season_games_subset["gameDate"] < pd.to_datetime("today").date()
        ]

        # Check if already populated, by doing this we save running DB inserts
        if self.con.execute(f"SELECT COUNT(*) FROM {table_name} WHERE season = '{season}'").fetchone()[0] == season_games_subset.shape[0]:
            logger.info(
                "Table %s already populated for season %s, skipping population.", table_name, season)
            return

        pre_persisted_game_ids = [season_game["game_id"] for season_game in self.sgd.get_season_games(
            season=season)]

        # Filter out already persisted games
        season_games_subset = season_games_subset[
            ~season_games_subset["gameId"].isin(pre_persisted_game_ids)
        ]

        # Clear existing entries for the season to avoid duplicates

        self.con.execute(
            f"INSERT INTO {table_name} SELECT * FROM season_games_subset")
        logger.info("Inserted season games for season %s", season)

    def perform_create_season_games_table(self, table_name: str):
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                game_id TEXT PRIMARY KEY,
                season TEXT,
                date DATE,
                game_status INT,
                game_label TEXT,
                home_team_id TEXT,
                home_team_abbreviation TEXT,
                home_team_score INT,
                away_team_id TEXT,
                away_team_abbreviation TEXT,
                away_team_score INT
            )
            """)
        print(f"Table {table_name} created successfully")

    def populate_box_score_datebase(self, season: str = "2024-25", overwrite_all_entries: bool = False):
        table_name = "box_score_traditional"

        self.perform_create_box_score_table(table_name=table_name)

        season_game_ids = self.sgd.get_season_games(season=season)

        if not overwrite_all_entries:
            # Make into set to get unique game_ids
            current_persisted_game_ids = set([box_score["game_id"] for
                                              box_score in self.bstr.fetch_all_box_scores_from_season(season=season)])

            print(
                f"{len(current_persisted_game_ids)} box scores out of {len(season_game_ids)} already saved in the database.")

            # Filter out the game_ids that are already persisted
            season_game_ids = [
                box_score for box_score in season_game_ids if box_score["game_id"] not in current_persisted_game_ids]

        for i, box_score in enumerate(season_game_ids):
            game_id = box_score["game_id"]
            logger.info("Attempting to persist %s", game_id)

            try:
                data = boxscoretraditionalv3.BoxScoreTraditionalV3(
                    game_id=game_id
                )
            except Exception as e:
                print(
                    f"Failed to fetch box score for game_id {game_id} due to error: {e}")
                raise ValueError from e

            box_score_traditional: pd.DataFrame = data.get_data_frames()[0]
            if not isinstance(box_score_traditional, pd.DataFrame):
                raise ValueError(
                    "Expected a pandas DataFrame from BoxScoreTraditionalV3 from the NBA API response.")

            box_score_data_subset = box_score_traditional.loc[:, [
                "gameId",
                # "season", # This is added in post-processing below
                "teamId",
                "personId",
                "nameI",
                "position",  # This field will have a value if they are a starter, else empty
                "minutes",
                "fieldGoalsMade",
                "fieldGoalsAttempted",
                "fieldGoalsPercentage",
                "threePointersMade",
                "threePointersAttempted",
                "threePointersPercentage",
                "freeThrowsMade",
                "freeThrowsAttempted",
                "freeThrowsPercentage",
                "reboundsOffensive",
                "reboundsDefensive",
                "reboundsTotal",  # 19
                "assists",  # 20
                "steals",
                "blocks",
                "turnovers",
                "foulsPersonal",
                "points",
                "plusMinusPoints"
            ]]
            box_score_data_subset["season"] = season
            box_score_data_subset["position"] = box_score_data_subset["position"].fillna(
                "").astype(bool)

            # Old code that broke when the minutes weren't correctly formatted
            # box_score_data_subset["minutes"] = box_score_data_subset["minutes"].apply(lambda x: int(
            #     x.split(":")[0]) * 60 + int(x.split(":")[1]) if isinstance(x, str) and ":" in x else 0)
            box_score_data_subset["minutes"] = box_score_data_subset["minutes"].apply(
                _parse_minutes)

            # Reorder columns to have gameId and season first
            column_order = [
                col for col in box_score_data_subset.columns if not col in ["gameId", "season"]]
            column_order = ["gameId", "season"] + column_order

            # Register the DataFrame as a named relation for DuckDB
            box_score_data_subset_reordered = box_score_data_subset[column_order]
            self.con.register("temp_box_score",
                              box_score_data_subset_reordered)
            self.con.execute(
                f"INSERT INTO {table_name} SELECT * FROM temp_box_score")

            logger.info(
                "Inserted box score for game_id %s. %d games remaining.", game_id, len(season_game_ids)-i-1)
            sleep(RATE_LIMIT_SLEEP_SECONDS)

    def perform_create_box_score_table(self, table_name: str):
        # player_id = personId from nba_api
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                game_id TEXT,
                season TEXT,
                team_id TEXT,
                player_id TEXT,
                player_name TEXT,
                starter BOOLEAN,
                seconds_played INT,
                field_goals_made INT,
                field_goals_attempted INT,
                field_goals_percentage DOUBLE,
                three_pointers_made INT,
                three_pointers_attempted INT,
                three_pointers_percentage DOUBLE,
                free_throws_made INT,
                free_throws_attempted INT,
                free_throws_percentage DOUBLE,
                offensive_rebounds INT,
                defensive_rebounds INT,
                total_rebounds INT,
                assists INT,
                steals INT,
                blocks INT,
                turnovers INT,
                personal_fouls INT,
                points INT,
                plus_minus_points DOUBLE
            )
            """)
        print(f"Table {table_name} created successfully")


def _parse_minutes(x):
    try:
        if isinstance(x, str) and ":" in x:
            mins, secs = x.split(":")
            return int(mins) * 60 + int(secs)
        elif isinstance(x, (int, float)):
            # already numeric
            return int(x)
    except TypeError:
        logger.warning("Failed to parse minutes value. Defaulting to -1")
    return -1  # fallback for invalid/missing data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NBA scraper script")
    parser.add_argument(
        "--season", help="NBA season to populate, e.g., '2023-24'")

    args = parser.parse_args()

    if args.season and re.match(r'^\d{4}-\d{2}$', args.season):
        season_to_populate = args.season
    else:
        season_to_populate = Utils.get_current_season()

    connection = None
    try:
        connection = duckdb.connect(database='nba_scraper.db', read_only=False)
        pdb = PopulateDatabase(connection)

        pdb.populate_all_databases(season=season_to_populate)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user. Exiting...")
    except ValueError as e:
        logger.error("An error occurred: %s", e)
    finally:
        if connection:
            connection.close()
