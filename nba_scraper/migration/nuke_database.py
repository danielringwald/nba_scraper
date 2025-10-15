import duckdb


def nuke_database_table(con, table_name: str):

    con.execute(f"DROP TABLE IF EXISTS {table_name};")


if __name__ == "__main__":
    con = duckdb.connect(database='nba_scraper.db', read_only=False)

    nuke_database_table(con, "total_box_scores_test1")
