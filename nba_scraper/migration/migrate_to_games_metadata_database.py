import time
import duckdb
import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH
import nba_scraper.migration.nuke_database as nd


def perform_create_table(con, table_name: str):
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            game_id VARCHAR NOT NULL,
            home_team VARCHAR NOT NULL,
            away_team VARCHAR NOT NULL
        )
        """)
    print(f"Table {table_name} created successfully")


if __name__ == "__main__":
    pass
