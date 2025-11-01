import re
from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import BOX_SCORE_TRADITIONAL_TABLE_NAME

from nba_scraper.dao.repository.common_repository import CommonRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameInformation

# TODO Change to use logging


class BoxScoreTraditionalRepository(CommonRepository):

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = BOX_SCORE_TRADITIONAL_TABLE_NAME
        self.team_name_repository = TeamNameRepository()

        print(f"{self.__class__.__name__} initialized")

    def fetch_box_score_by_team_and_season(self, team_id: str = None, season: str = None) -> list[tuple]:
        team_id = self._transform_team_id(team_id=team_id)

        if not season or season == "":
            season = Utils.get_current_season()

        self._validate_season_format(season=season)

        where_parameters = {"team_id": team_id, "season": season}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        return result or []

    def fetch_all_box_scores_from_season(self, season: str = None) -> list[tuple]:
        # Validation
        self._validate_season_format(season)

        where_parameters = {"season": season}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        return result or []

    def _transform_team_id(self, team_id: str):
        if not team_id:
            raise ValueError("Must provide a valid team_id")

        if re.match(r"^[A-Z]{3}$", team_id):
            return TeamNameInformation(*self.team_name_repository.get_team_information(
                team_id)).get_team_id()

        if re.match(r"^\d{10}$", team_id):
            return team_id

        raise ValueError(
            "team_id has to be a 3-letter abbreviation or a 10 digit ID")
