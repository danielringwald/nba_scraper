import duckdb
from duckdb import DuckDBPyConnection


def test_database(con: DuckDBPyConnection, table_name: str):

    print(con.execute(
        f"SELECT * FROM {table_name} WHERE game_id = '202310240DEN_DEN'").fetch_df())


if __name__ == "__main__":
    test_database(duckdb.connect(
        database='nba_scraper.db', read_only=False), "total_box_scores_test1")
