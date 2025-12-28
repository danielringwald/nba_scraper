import logging
from nba_scraper.configuration.database_config import SEASON_GAMES_TABLE_NAME
from nba_scraper.dao.repository.common_repository import CommonRepository

logger = logging.getLogger(__name__)


class SeasonGamesRepository(CommonRepository):
    """
        Repository class for season games data access
    """

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = SEASON_GAMES_TABLE_NAME

        logger.info("%s initialized", self.__class__.__name__)

    def get_season_games(self, season: str) -> list[tuple] | list[dict[str, str]]:
        """
            DuckDB implementation of Python DB API specification, https://peps.python.org/pep-0249/, returns a tuple
            that is why we type hint the tuple list.
        """

        # Validation
        self._validate_season_format(season)

        where_clause_parameters = {"season": season}

        result = self._database_select_all(where_clause_parameters)

        return self._return_list_or_empty(result)

    def get_single_game(self, game_id: str) -> tuple:
        """
            Get a single game by its game_id
        """

        where_clause_parameters = {"game_id": game_id}

        result = self._database_select_one(where_clause_parameters)

        return self._return_tuple_or_empty(result)

    def get_games_by_team(self, team_id: str, limit: int = 5) -> list[tuple] | list[dict[str, str]]:
        """
            Get all the games for the specified team (both home and away)
        """

        where_clause_parameters = {
            "OR": {"home_team_id": team_id, "away_team_id": team_id}}

        result = self._database_select_all(
            where_clause_parameter_map=where_clause_parameters)[0:limit]

        formatted_result = self._return_list_or_empty(result)

        # Sort the list by date descending
        formatted_result.sort(key=lambda x: x['date'], reverse=True)

        return formatted_result
