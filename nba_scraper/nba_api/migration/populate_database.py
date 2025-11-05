from time import sleep
import duckdb
import pandas as pd
import regex as re

from nba_api.stats.library.data import teams as NBA_TEAMS
from nba_api.stats.endpoints import scheduleleaguev2
from nba_api.stats.endpoints import boxscoretraditionalv3

import nba_scraper.migration.nuke_database as nd
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
from nba_scraper.configuration.database_config import TEAM_NAME_INFORMATION_TABLE_NAME

RATE_LIMIT_SLEEP_SECONDS = 1


class PopulateDatabase:

    def __init__(self, con: duckdb.DuckDBPyConnection):
        self.con = con
        self.sgd = SeasonGamesRepository()
        self.bstr = BoxScoreTraditionalRepository()

    def populate_all_databases(self):
        season = "2024-25"
        self.populate_all_databases()
        self.populate_season_games_datebase(
            season=season, exclude_game_labels=["Preseason"])
        self.populate_box_score_datebase(season=season)

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

            self.con.execute(
                f"INSERT INTO {table_name} SELECT * FROM df")
            print("Inserted team:", team_name)

    def perform_create_teams_information_table(self, table_name: str):
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                team_id TEXT PRIMARY KEY,
                team_abbreviation TEXT,
                team_name TEXT
            )
            """)
        print(f"Table {table_name} created successfully")

    # Games Schedule

    def populate_season_games_datebase(self, season: str = "2024-25", exclude_game_labels: list[str] = []):
        # TODO Extend to support multiple seasons, remember to update method populate_all_databases

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
            print(
                f"Table {table_name} already populated for season {season}, skipping population.")
            return

        self.con.execute(
            f"INSERT INTO {table_name} SELECT * FROM season_games_subset")
        print(f"Inserted season games for season {season}")

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
            current_persisted_game_ids = set([game_id for (
                game_id, *_) in self.bstr.fetch_all_box_scores_from_season(season=season)])

            print(
                f"{len(current_persisted_game_ids)} box scores out of {len(season_game_ids)} already saved in the database.")

            # Filter out the game_ids that are already persisted
            season_game_ids = [
                box_score for box_score in season_game_ids if box_score[0] not in current_persisted_game_ids]

        for i, (game_id, *_) in enumerate(season_game_ids):
            try:
                data = boxscoretraditionalv3.BoxScoreTraditionalV3(
                    game_id=game_id
                )
            except Exception as e:
                print(
                    f"Failed to fetch box score for game_id {game_id} due to error: {e}")
                raise Exception from e
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
                "reboundsTotal",
                "assists",
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
            box_score_data_subset["minutes"] = box_score_data_subset["minutes"].apply(lambda x: int(
                x.split(":")[0]) * 60 + int(x.split(":")[1]) if isinstance(x, str) and ":" in x else 0)

            # Reorder columns to have gameId and season first
            column_order = [
                col for col in box_score_data_subset.columns if not col in ["gameId", "season"]]
            column_order = ["gameId", "season"] + column_order

            # This field is used in the connection query
            box_score_data_subset_reordered = box_score_data_subset[column_order]

            self.con.execute(
                f"INSERT INTO {table_name} SELECT * FROM box_score_data_subset_reordered")
            print(
                f"Inserted box score for game_id {game_id}. {len(season_game_ids)-i-1} games remaining.")
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


if __name__ == "__main__":
    connection = duckdb.connect(database='nba_scraper.db', read_only=False)
    pdb = PopulateDatabase(connection)

    nuke_database_tables = [
        #    "box_score_traditional",
        #    "season_games",
        #    "teams_information",
        #    "test_box_scores",
        #    "test_schedule_and_results"
    ]
    if len(nuke_database_tables) > 0:
        for tn in nuke_database_tables:
            print(f"Dropping table: {tn}")
            nd.nuke_database_table(connection, tn)

    season = "2025-26"

    pdb.populate_teams_information_datebase()
    pdb.populate_season_games_datebase(
        season=season, exclude_game_labels=["Preseason"])

    tries = 3
    for attempt in range(tries):
        try:
            pdb.populate_box_score_datebase(
                season=season)
            break
        except Exception as e:
            print(
                f"Attempt {attempt + 1} of {tries} failed with error: {e}")
            if attempt < tries - 1:
                print("Retrying...")
                sleep(5)
            else:
                print("All attempts failed.")
