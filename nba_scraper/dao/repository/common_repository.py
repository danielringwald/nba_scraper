from abc import ABC
import duckdb
import re

from nba_scraper.configuration.database_config import DATABASE_PATH


class CommonRepository(ABC):
    """
        Abstract common class for repositories
    """

    TABLE_NAME = None

    def __init__(self):
        self.con = duckdb.connect(database=DATABASE_PATH, read_only=False)

    def _validate_season_format(self, season: str) -> None:

        match = re.fullmatch(r"^(19|20)(\d{2})-(\d{2})$", season)
        if not match:
            raise ValueError(
                "Invalid season format. Must be in 'YYYY-YY' format.")

        year_start = int(match.group(2))
        year_end = int(match.group(3))
        # handle wrap-around like 1999–00
        if (year_start + 1) % 100 != year_end:
            raise ValueError(
                f"Invalid season range: {season}. Expected consecutive years.")

    def _database_select_all(self, where_clause_parameter_map: dict[str, any] = None) -> list[tuple]:
        """
            where_clause takes arguemnts as a dict where the key is the column and the value is the value of the column
        """
        return self._database_perform_select(where_clause_parameter_map).fetchall()

    def _database_select_one(self, where_clause_parameter_map: dict[str, any]):
        """
            where_clause takes arguemnts as a dict where the key is the column and the value is the value of the column
        """
        return self._database_perform_select(where_clause_parameter_map).fetchone()

    def _database_perform_select(self, where_clause_parameter_map: dict[str, any] = None) -> duckdb.DuckDBPyConnection:
        if where_clause_parameter_map is None:
            # Due to a dict being mutable we cannot use it as a default parameter
            # Calling function without where clause could modify the default parameter for future calls
            where_clause_parameter_map = {}

        where_clause, where_parameters = self._create_where_clause(
            where_clause_parameter_map=where_clause_parameter_map)

        query = f"SELECT * FROM {self.TABLE_NAME} {where_clause};"

        query_result = self.con.execute(query, where_parameters)

        if not query_result:
            print(
                f"WARN: No results for query: {query} Parameters: {where_clause_parameter_map}")

        return query_result

    def _create_where_clause(self, where_clause_parameter_map: dict[str, any]) -> str:
        resulting_where_clause = ""
        resulting_parameters = []

        if len(where_clause_parameter_map) > 0:

            # Add leading where to make it easier to add the "AND"s
            resulting_where_clause += "WHERE 1=1 "

            for k in where_clause_parameter_map:
                resulting_where_clause += f"AND {k} = ? "
                resulting_parameters += [where_clause_parameter_map.get(k)]

        return resulting_where_clause, resulting_parameters
