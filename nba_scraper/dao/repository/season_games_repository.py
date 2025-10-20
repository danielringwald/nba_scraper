from nba_scraper.configuration.database_config import SEASON_GAMES_TABLE_NAME
from nba_scraper.dao.repository.common_repository import CommonRepository


class SeasonGamesRepository(CommonRepository):

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = SEASON_GAMES_TABLE_NAME
        print(f"{self.__class__.__name__} initialized")

    def get_season_games(self, season: str) -> list[tuple]:
        """
            duckdb implementation of Python DB API specification, https://peps.python.org/pep-0249/, returns a tuple
            that is why we type hint the tuple list.
        """

        # Validation
        self._validate_season_format(season)

        where_clause_parameters = {"season": season}

        result = self._database_select_all(where_clause_parameters)

        # list is truthy so if empty it will be false
        if not result:
            print(
                f"WARN: No games found for season {season}. Result: {result}")
            return []

        return result
