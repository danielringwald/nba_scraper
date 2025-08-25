import duckdb
import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH

rename_columns_mapping = {
    "3P": "THREE_P",
    "3PA": "THREE_PA",
    "3P%": "THREE_P_PERCENT",
    "FG%": "FG_PERCENT",
    "FT%": "FT_PERCENT",
    "+/-": "plus_minus"
}


def save_box_score_to_database(con):
    df = pd.read_csv(
        'nba_scraper/data/box_score/total_box_scores/201910220LAC_LAC.csv')

    df["game_id"] = "201910220LAC_LAC"

    cols = ["game_id"] + [c for c in df.columns if c != "game_id"]
    df = df[cols]

    df.rename(columns=rename_columns_mapping, inplace=True)

    con.execute(
        "INSERT INTO total_box_scores SELECT * FROM df")


def main():
    con = duckdb.connect(database='nba_scraper.db', read_only=False)

#   game_id    │  Starters      │      MP      │   FG   │  FGA   │  FG%   │   3P   │  3PA   │  3P%   │   FT   │  FTA   │  FT%   │  ORB   │  DRB   │  TRB   │  AST   │  STL   │  BLK   │  TOV   │   PF   │  PTS   │  GmSc  │  +/-   │
#   varchar    │   varchar      │   varchar    │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │ double │
    con.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        game_id VARCHAR,
        Starters VARCHAR,
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

    box_score_games = Utils.get_csv_files_from_directory(TOTAL_BOX_SCORES_PATH)
