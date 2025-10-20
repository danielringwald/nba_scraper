import regex as re
from nba_scraper.dao.repository.common_repository import CommonRepository
from nba_scraper.configuration.database_config import TEAM_NAME_INFORMATION_TABLE_NAME


class TeamNameRepository(CommonRepository):
    # TODO Make the varibale TEAM_NAME_INFORMATION_TABLE_NAME be in the docstrings
    """

        Database schema for team_name_information
        CREATE TABLE IF NOT EXISTS {TEAM_NAME_INFORMATION_TABLE_NAME} (
                team_id TEXT PRIMARY KEY,
                team_abbreviation TEXT,
                team_name TEXT
        )
    """

    def __init__(self):
        super().__init__()
        self.TABLE_NAME = TEAM_NAME_INFORMATION_TABLE_NAME

        print(f"{self.__class__.__name__} initialized")

    def get_team_information(self, team_id: str | int) -> str | None:
        if re.match(r'^[A-Z]{3}$', str(team_id)):
            query = "SELECT * FROM teams_information WHERE team_abbreviation = ?"
        elif re.match(r'^\d{10}$', str(team_id)):
            query = "SELECT * FROM teams_information WHERE team_id = ?"
        else:
            raise ValueError(
                "Invalid team_id format. Must be a 3-letter abbreviation or a 10-digit team ID.")

        where_clause_paramteres = {"team_id": team_id}
        return self._database_select_one(where_clause_paramteres)


class TeamNameInformation:

    def __init__(self, team_id: str, team_abbreviation: str, team_name: str):
        if not isinstance(team_id, str):
            raise ValueError("team_id has to of type str")
        if not isinstance(team_abbreviation, str):
            raise ValueError("team_abbreviation has to of type str")
        if not isinstance(team_name, str):
            raise ValueError("team_name has to of type str")

        self.team_id: str = team_id
        self.team_abbreviation: str = team_abbreviation
        self.team_name: str = team_name

    def get_team_id(self) -> str:
        return self.team_id

    def get_team_abbreviation(self) -> str:
        return self.team_abbreviation

    def get_team_name(self) -> str:
        return self.team_name
