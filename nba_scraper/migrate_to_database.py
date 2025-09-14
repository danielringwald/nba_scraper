import duckdb
import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH

rename_columns_mapping = {
    "Starters": "player_name",
    "3P": "THREE_P",
    "3PA": "THREE_PA",
    "3P%": "THREE_P_PERCENT",
    "FG%": "FG_PERCENT",
    "FT%": "FT_PERCENT",
    "+/-": "plus_minus"
}


def save_box_score_to_database(con, file_name: str, table_name: str, create_table: bool = False):
    """
        file_name: str
            Example: 201910220LAC_LAC.csv # Needs to end in .csv otherwise will break
    """

    df = pd.read_csv(
        'nba_scraper/data/box_score/total_box_scores/' + file_name)

    df["game_id"] = file_name.split(".csv")[0]
    df["starter"] = [True]*5 + [False]*(len(df)-5)

    cols = ["game_id", "Starters", "starter"] + \
        [c for c in df.columns if c not in ["game_id", "Starters", "starter"]]

    df = df[cols]

    df.rename(columns=rename_columns_mapping, inplace=True)

    if create_table:
        con.execute(
            f"INSERT INTO {table_name} SELECT * FROM df")

        print(f"Inserted {len(df)} rows from {file_name} into the database.")
    else:
        print(df)
        print("Table creation and data entry skipped.")


def perform_create_table(con, table_name: str):
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            game_id VARCHAR NOT NULL,
            player_name VARCHAR,
            starter BOOLEAN,
            MP VARCHAR,
            FG DOUBLE,
            FGA DOUBLE,
            FG_PERCENT DOUBLE,
            THREE_P DOUBLE,
            THREE_PA DOUBLE,
            THREE_P_PERCENT DOUBLE,
            FT DOUBLE,
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
    print("Table created successfully")


def main(table_name: str, create_table: bool = False):
    con = duckdb.connect(database='nba_scraper.db', read_only=False)

#   game_id    │  Starters      │      MP      │   FG   │  FGA   │  FG%   │   3P   │  3PA   │  3P%   │   FT   │  FTA   │  FT%   │  ORB   │  DRB   │  TRB   │  AST   │  STL   │  BLK   │  TOV   │   PF   │  PTS   │  GmSc  │  +/-   │
#   varchar    │   varchar      │   varchar    │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │
    if create_table:
        perform_create_table(con, table_name)

    box_score_games = Utils.get_csv_files_from_directory(TOTAL_BOX_SCORES_PATH)
    print(box_score_games[:5])
    save_box_score_to_database(
        con, "201910220LAC_LAC.csv", table_name, create_table)


if __name__ == "__main__":
    main(table_name="total_box_scores_test1", create_table=True)
