import regex as re
from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import BOX_SCORE_TRADITIONAL_TABLE_NAME

from nba_scraper.dao.repository.common_repository import CommonRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameInformation


class BoxScoreTraditionalRepository(CommonRepository):

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = BOX_SCORE_TRADITIONAL_TABLE_NAME
        self.team_name_repository = TeamNameRepository()

        print(f"{self.__class__.__name__} initialized")

    def fetch_box_score_from_team_and_season(self, team_id: str = None, season: str = None) -> list[tuple]:
        if not team_id:
            raise ValueError("Must provide a valid team_id")

        if re.match(r"^[A-Z]{3}$", team_id):
            team_id = TeamNameInformation(*self.team_name_repository.get_team_information(
                team_id)).get_team_id()
        elif not re.match(r"^\d{10}$", team_id):
            raise ValueError(
                "team_id has to be a 3-letter abbreviation or a 10 digit ID")

        if not season or season == "":
            season = Utils.get_current_season()

        self._validate_season_format(season=season)

        where_parameters = {"team_id": team_id, "season": season}
        result = self._database_select_all(
            where_clause_parameter_map=where_parameters)

        # list is truthy so if empty it will be false
        if not result:
            print(
                f"WARN: No box score games found for season {season}. Parameters: {where_parameters}")
            return []

        return result

    def fetch_all_box_scores_from_season(self, season: str = None) -> list[tuple]:
        # Validation
        self._validate_season_format(season)

        query = "SELECT * FROM box_score_traditional WHERE season = ?"
        result = self.con.execute(query, [season]).fetchall()

        # list is truthy so if empty it will be false
        if not result:
            print(
                f"WARN: No games found for season {season}. Query: {query} Parameters: {[season]}")
            return []

        return result
