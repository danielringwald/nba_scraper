import logging
from nba_scraper.configuration.database_config import SEASON_GAMES_TABLE_NAME
from nba_scraper.dao.repository.common_repository import CommonRepository

logger = logging.getLogger(__name__)


class SeasonGamesRepository(CommonRepository):

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = SEASON_GAMES_TABLE_NAME

        logger.info("%s initialized", self.__class__.__name__)

    def get_season_games(self, season: str, include_columns: bool = True) -> list[tuple]:
        """
            DuckDB implementation of Python DB API specification, https://peps.python.org/pep-0249/, returns a tuple
            that is why we type hint the tuple list.
        """

        # Validation
        self._validate_season_format(season)

        where_clause_parameters = {"season": season}

        result = self._database_select_all(where_clause_parameters)

        # list is truthy so if empty it will be false
        if not result:
            logger.warning(
                "No games found for season %s. Result: %s", season, result)
            return []

        return self._format_result(result, include_columns=include_columns)

    def get_single_game(self, game_id: str, include_columns: bool = True) -> tuple:
        where_clause_parameters = {"game_id": game_id}

        result = self._database_select_one(where_clause_parameters)

        if not result:
            logger.warning(
                "No game found for game_id %s. Result: %s", game_id, result)
            return ()

        return self._format_result(result, include_columns=include_columns)

    def get_games_by_team(self, team_id: str, limit: int = 5, include_columns: bool = True) -> list[tuple] | list[dict[str, str]]:
        where_clause_parameters = {
            "OR": {"home_team_id": team_id, "away_team_id": team_id}}
        result = self._database_select_all(
            where_clause_parameter_map=where_clause_parameters)[0:limit]

        if not result:
            logger.warning(
                "No games found for team_id %s. Result: %s", team_id, result)
            return []

        response = self._format_result(result, include_columns=include_columns)

        # Sort the list by date descending, HARD dependency on included columns being true
        response.sort(key=lambda x: x['date'], reverse=True)

        return response
