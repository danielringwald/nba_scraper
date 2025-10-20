import time
import duckdb
import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.configuration.global_config import NBA_TEAM_FULL_NAME_TO_ABBRIV
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH
from nba_scraper.configuration.schedule_and_results import SCHEDULE_AND_RESULTS_PATH
import nba_scraper.migration.nuke_database as nd

rename_box_score_columns_mapping = {
    "Starters": "player_name",
    "3P": "THREE_P_MADE",
    "3PA": "THREE_P_ATTP",
    "3P%": "THREE_P_PERCENT",
    "FG%": "FG_PERCENT",
    "FT%": "FT_PERCENT",
    "+/-": "plus_minus"
}

BOX_SCORE_TABLE_NAME = "test_box_scores"

rename_schedule_and_results_columns_mapping = {
    "Date": "date",
    "Visitor/Neutral": "away_team",
    "PTS": "away_team_score",
    "Home/Neutral": "home_team",
    "PTS.1": "home_team_score"
}

schedule_and_results_column_order = [
    "game_id",
    "date",
    "home_game_id",
    "home_team",
    "home_team_score",
    "away_game_id",
    "away_team",
    "away_team_score",
    "winner"]

SCHEDULE_AND_RESULTS_TABLE_NAME = "test_schedule_and_results"


##### BOX SCORE METHODS #####


def save_season_of_box_scores_to_database(con, seasons: int | list[int], table_name: str, perform_inserts: bool = True):
    seasons = Utils.to_list(seasons)

    for season in seasons:
        start_time = time.time()
        box_score_games = Utils.get_csv_files_from_directory_and_season(
            TOTAL_BOX_SCORES_PATH, season)
        save_list_of_box_scores_to_database(
            con, file_names=box_score_games, table_name=table_name, perform_inserts=perform_inserts)

        end_time = time.time()
        print(
            f"Finished inserting box scores for season {season} to database.\nTook {(end_time-start_time)} s")


def save_list_of_box_scores_to_database(con, file_names: list[str], table_name: str, perform_inserts: bool = True):
    number_of_files_to_migrate = len(file_names)

    for i, file_name in enumerate(file_names):
        save_box_score_to_database(
            con, file_name=file_name, table_name=table_name, perform_inserts=perform_inserts)

        if i % 100 == 0:
            print(
                f"Finished inserting {i} of out {number_of_files_to_migrate} files into DB.")

    print(
        f"Finished inserting {number_of_files_to_migrate} number of files into {table_name} database.")


def save_box_score_to_database(con, file_name: str, table_name: str, perform_inserts: bool = False):
    """
        file_name: str
            Example: 201910220LAC_LAC.csv or 201910220LAC_LAC 
    """

    if not file_name.endswith(".csv"):
        file_name = file_name + ".csv"

    df = pd.read_csv(
        TOTAL_BOX_SCORES_PATH + file_name)

    df["team_game_id"] = file_name.split(".csv")[0]
    df["starter"] = [True] * 5 + [False] * (len(df) - 5)
    df["date"] = file_name[0:4] + "-" + file_name[4:6] + "-" + file_name[6:8]

    cols = ["team_game_id", "date", "Starters", "starter"] + \
        [c for c in df.columns if c not in [
            "team_game_id", "date", "Starters", "starter"]]

    df = df[cols]

    df.rename(columns=rename_box_score_columns_mapping, inplace=True)

    if perform_inserts:
        con.execute(
            f"INSERT INTO {table_name} SELECT * FROM df")

        # print(f"Inserted {len(df)} rows from {file_name} into the database.")
    else:
        print(df)
        print("Insert statements skipped.")


def perform_create_box_score_table(con, table_name: str):
    # TODO Change "date" column to be an actual date to easily be able to query using schedule and results
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            game_id VARCHAR NOT NULL,
            date DATE,
            player_name VARCHAR,
            starter BOOLEAN,
            MP VARCHAR,
            FG_MADE DOUBLE,
            FGA DOUBLE,
            FG_PERCENT DOUBLE,
            THREE_P_MADE DOUBLE,
            THREE_P_ATTP DOUBLE,
            THREE_P_PERCENT DOUBLE,
            FT_MADE DOUBLE,
            FTA DOUBLE,
            FT_PERCENT DOUBLE,
            ORB DOUBLE,
            DRB DOUBLE,
            TRB DOUBLE,
            AST DOUBLE,
            STL DOUBLE,
            BLK DOUBLE,
            TOV DOUBLE,
            PF DOUBLE,
            PTS DOUBLE,
            GmSc DOUBLE,
            plus_minus DOUBLE
        )
        """)
    print(f"Table {table_name} created successfully")

##### SCHEDULE AND RESULTS METHODS #####


def save_season_of_scedhule_and_results_to_database(con, seasons: int | list[int], table_name: str, perform_inserts: bool = True):
    seasons = Utils.to_list(seasons)

    for season in seasons:
        start_time = time.time()
        schedule_and_results = Utils.get_schedule_and_results_csv_for_single_season(
            SCHEDULE_AND_RESULTS_PATH, season)
        save_list_of_schedule_and_results_to_database(
            con, file_names=schedule_and_results, table_name=table_name, perform_inserts=perform_inserts)

        end_time = time.time()
        print(
            f"Finished inserting schedule and results for season {season} into {table_name} database.\nTook {(end_time-start_time):.4} s")


def save_list_of_schedule_and_results_to_database(con, file_names: list[str], table_name: str, perform_inserts: bool = True):
    number_of_files_to_migrate = len(file_names)

    for i, file_name in enumerate(file_names):
        save_schedule_and_results_to_database(
            con, file_name=file_name, table_name=table_name, perform_inserts=perform_inserts)

        print(
            f"Finished inserting {i} of out {number_of_files_to_migrate} files into {table_name} DB.")


def save_schedule_and_results_to_database(con, file_name: str, table_name: str, perform_inserts: bool = False):
    """
        file_name: str
            Example: 2025_march_games_result.csv or 2025_march_games_result 
    """

    if not file_name.endswith(".csv"):
        file_name = file_name + ".csv"

    df = pd.read_csv(
        SCHEDULE_AND_RESULTS_PATH + file_name)

    df = parse_schedule_and_results_to_database_format(df)

    df = df.rename(columns=rename_schedule_and_results_columns_mapping)

    df = df[schedule_and_results_column_order]

    if perform_inserts:
        con.execute(
            f"INSERT INTO {table_name} SELECT * FROM df")

        print(f"Inserted {len(df)} rows from {file_name} into the database.")
    else:
        print(df)
        print("Insert statements skipped.")


def parse_schedule_and_results_to_database_format(df: pd.DataFrame):
    # Convert to YYYY-MM-DD date format
    df["Date"] = pd.to_datetime(df["Date"])

    # Create game_id using home team and date.
    # Magic zero is added since that is how bbref stores the gameIds

    # TODO THIS GIVES SOME NANs FOR SOME REASON INVESTIGATE, DID THE CHANGE IN THE DATE PARSING CAUSE THIS?
    print(df["Home/Neutral"].to_string())
    df["game_id"] = df["Date"].apply(lambda v: str(v.date()).replace("-", "")) + \
        df["Home/Neutral"].apply(lambda v: "0" +
                                 NBA_TEAM_FULL_NAME_TO_ABBRIV[v])
    # Convert home team name to team abbriviation
    df["Home/Neutral"] = df["Home/Neutral"].apply(
        lambda v: NBA_TEAM_FULL_NAME_TO_ABBRIV[v])

    # Generate home game ID that is the key to find box scores in box score DB
    df["home_game_id"] = df["game_id"] + "_" + df["Home/Neutral"]

    # Convert away team name to team abbriviation
    df["Visitor/Neutral"] = df["Visitor/Neutral"].apply(
        lambda v: NBA_TEAM_FULL_NAME_TO_ABBRIV[v])

    # Generate away game ID that is the key to find box scores in box score DB
    df["away_game_id"] = df["game_id"] + "_" + df["Visitor/Neutral"]

    # Parse the winner and store in columnd
    df["winner"] = df.apply(
        lambda row: row["Visitor/Neutral"] if row["PTS"] > row["PTS.1"] else row["Home/Neutral"],
        axis=1
    )

    return df


def perform_create_schedule_and_stats_table(con, table_name: str):
    # TODO Change "date" to be a date type
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            game_id VARCHAR NOT NULL,
            date DATE,
            home_game_id VARCHAR,
            home_team VARCHAR,
            home_team_score INTEGER,
            away_game_id VARCHAR,
            away_team VARCHAR,
            away_team_score INTEGER,
            winner VARCHAR
            )
            """)

    print(f"Table {table_name} created successfully")


def perform_database_table_drops_if_relevant(con, nuke_database_tables: list[str] | str):
    Utils.to_list(nuke_database_tables)
    if len(nuke_database_tables) > 0:
        for table_name in nuke_database_tables:
            print(f"Dropping table: {table_name}")
            nd.nuke_database_table(con, table_name)


def main(perform_inserts: bool = True, create_table: bool = False, nuke_database_tables: list[str] = []):
    con = duckdb.connect(database='nba_scraper.db', read_only=False)
    perform_database_table_drops_if_relevant(con, nuke_database_tables)

#   game_id    │  Starters      │      MP      │   FG   │  FGA   │  FG%   │   3P   │  3PA   │  3P%   │   FT   │  FTA   │  FT%   │  ORB   │  DRB   │  TRB   │  AST   │  STL   │  BLK   │  TOV   │   PF   │  PTS   │  GmSc  │  +/-   │
#   varchar    │   varchar      │   varchar    │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │
    if create_table:
        perform_create_box_score_table(
            con, BOX_SCORE_TABLE_NAME)

        perform_create_schedule_and_stats_table(
            con, SCHEDULE_AND_RESULTS_TABLE_NAME)

    # save_season_of_box_scores_to_database(
    #     con, seasons=2024, table_name=BOX_SCORE_TABLE_NAME, perform_inserts=perform_inserts)

    save_season_of_scedhule_and_results_to_database(
        con, seasons=2024, table_name=SCHEDULE_AND_RESULTS_TABLE_NAME, perform_inserts=perform_inserts)


if __name__ == "__main__":
    main(create_table=True,
         nuke_database_tables=[BOX_SCORE_TABLE_NAME, SCHEDULE_AND_RESULTS_TABLE_NAME])
