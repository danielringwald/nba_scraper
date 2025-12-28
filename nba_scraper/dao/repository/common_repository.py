from abc import ABC
import duckdb
import re
import logging

from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import DATABASE_PATH

logger = logging.getLogger(__name__)


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

    def _database_select_all(self, where_clause_parameter_map: dict[str, any] = None, order_by: str = None) -> list[tuple]:
        """
            where_clause takes arguemnts as a dict where the key is the column and the value is the value of the column
        """
        return self._database_perform_select(where_clause_parameter_map, order_by).fetchall()

    def _database_select_one(self, where_clause_parameter_map: dict[str, any]):
        """
            where_clause takes arguemnts as a dict where the key is the column and the value is the value of the column
        """
        return self._database_perform_select(where_clause_parameter_map).fetchone()

    def _database_perform_select(self, where_clause_parameter_map: dict[str, any] = None, order_by: str = None) -> duckdb.DuckDBPyConnection:
        if where_clause_parameter_map is None:
            # Due to a dict being mutable we cannot use it as a default parameter
            # Calling function without where clause could modify the default parameter for future calls
            where_clause_parameter_map = {}

        if order_by:
            order_by_clause = f" ORDER BY {order_by} DESC"
        else:
            order_by_clause = ""

        where_clause, where_parameters = self._create_where_clause(
            where_clause_parameter_map=where_clause_parameter_map)

        query = f"SELECT * FROM {self.TABLE_NAME} {where_clause} {order_by_clause};"

        query_result = self.con.execute(query, where_parameters)

        if not query_result:
            logger.warning(
                "No results for query: %s Parameters: %s", query, where_clause_parameter_map)

        return query_result

    def _create_where_clause(self, where_clause_parameter_map: dict[str, any]) -> tuple[str, list[str]]:
        """
            If where_clause_parameter_map is just key-values, then it will default to "AND" logic. 

            Accepts structured dict with AND and OR:
            {
                "AND": {
                    "column1": "value1"
                    "column2": "value2"
                },
                "OR": {
                    "column3": "value3"
                    "column4": "value4"
                }
            }
        """
        if not where_clause_parameter_map:
            return "", []

        parameters = []
        clauses = []

        # Case 1: New nested syntax using AND / OR groups
        if "AND" in where_clause_parameter_map or "OR" in where_clause_parameter_map:
            if "AND" in where_clause_parameter_map:
                and_parts = []
                for col, val in where_clause_parameter_map["AND"].items():
                    and_parts.append(f"{col} = ?")
                    parameters.append(val)
                clauses.append("(" + " AND ".join(and_parts) + ")")

            if "OR" in where_clause_parameter_map:
                or_parts = []
                for col, val in where_clause_parameter_map["OR"].items():
                    or_parts.append(f"{col} = ?")
                    parameters.append(val)
                clauses.append("(" + " OR ".join(or_parts) + ")")

            final_clause = "WHERE " + " AND ".join(clauses)
            print(final_clause, parameters)
            return final_clause, parameters

        # Case 2: Old simple flat dict → AND logic
        base_clause = "WHERE 1=1"
        for col, val in where_clause_parameter_map.items():
            base_clause += f" AND {col} = ?"
            parameters.append(val)

        return base_clause, parameters

    def get_table_columns(self) -> list[str]:
        rows = self.con.execute(
            f"PRAGMA table_info('{self.TABLE_NAME}')").fetchall()
        return [row[1] for row in rows]

    def _format_result(self, result: list[tuple], include_columns: bool = True) -> list[tuple] | list[dict[str, str]]:
        result = Utils.to_list(result)

        if include_columns:
            column_names = self.get_table_columns()
            return [dict(zip(column_names, row)) for row in result]
        return result

    def _return_tuple_or_empty(self, result: tuple | None) -> tuple:
        if not result:
            return ()
        return self._format_result(result)

    def _return_list_or_empty(self, result: list[tuple]) -> list[tuple] | list[dict[str, str]]:
        if not result:
            return []
        return self._format_result(result)
