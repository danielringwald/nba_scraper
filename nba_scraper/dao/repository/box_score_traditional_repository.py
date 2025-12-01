import logging
import duckdb

from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import BOX_SCORE_TRADITIONAL_TABLE_NAME
from nba_scraper.dao.repository.common_repository import CommonRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository


logger = logging.getLogger(__name__)


class BoxScoreTraditionalRepository(CommonRepository):
    """
        Database schema for box score traditional repository, table name specified by BOX_SCORE_TRADITIONAL_TABLE_NAME

        SQL schema:
        CREATE TABLE IF NOT EXISTS {BOX_SCORE_TRADITIONAL_TABLE_NAME} (
                game_id TEXT,
                season TEXT,
                team_id TEXT,
                player_id TEXT,
                player_name TEXT,
                starter BOOLEAN,
                seconds_played INT,
                field_goals_made INT,
                field_goals_attempted INT,
                field_goals_percentage DOUBLE,
                three_pointers_made INT,
                three_pointers_attempted INT,
                three_pointers_percentage DOUBLE,
                free_throws_made INT,
                free_throws_attempted INT,
                free_throws_percentage DOUBLE,
                offensive_rebounds INT,
                defensive_rebounds INT,
                total_rebounds INT,
                assists INT,
                steals INT,
                blocks INT,
                turnovers INT,
                personal_fouls INT,
                points INT,
                plus_minus_points DOUBLE
            )
    """

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = BOX_SCORE_TRADITIONAL_TABLE_NAME
        self.team_name_repository = TeamNameRepository()

        logger.info("%s initialized", self.__class__.__name__)
        try:
            logger.info("Box score traditional columns: %s",
                        self.get_table_columns())
        except duckdb.Error as e:
            logger.error("Error fetching table columns: %s", e)

    def fetch_box_score_by_team_and_season(self, team_id: str = None, season: str = None) -> list[tuple]:
        if not season:
            season = Utils.get_current_season()

        self._validate_season_format(season=season)

        where_parameters = {"team_id": team_id, "season": season}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        return self._return_list_or_empty(result)

    def fetch_all_box_scores_from_season(self, season: str = None) -> list[tuple] | list[dict[str, str]]:
        # Validation
        self._validate_season_format(season)

        where_parameters = {"season": season}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        return self._return_list_or_empty(result)

    def fetch_all_box_scores_for_team(self, team_id: str = None, limit: int = 5) -> list[tuple]:
        where_parameters = {
            "OR": {"home_team_id": team_id, "away_team_id": team_id}}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)[0:limit]

        return self._return_list_or_empty(result)

    def fetch_all_box_scores_for_game_id(self, game_id: str) -> list[tuple]:
        where_parameters = {"game_id": game_id}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        return self._return_list_or_empty(result)
