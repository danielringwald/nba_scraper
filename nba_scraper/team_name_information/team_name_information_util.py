from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import TeamInformationColumn as tic
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository


class TeamNameInformationUtil:

    def __init__(self):
        self.team_name_repository = TeamNameRepository()

    def convert_team_id_to_small_number(self, team_id: str | list[str]) -> list[int]:
        """
            Converts team IDs to a smaller numerical representation to better fit ML models.
        """

        team_ids: list[str] = Utils.to_list(team_id)

        all_teams = self.team_name_repository.get_all_teams_information()

        # All teams have unqieu last 2 digits, i.e. to get the last two we can use modulo 100
        team_number_representation = [
            int(team_id[tic.TEAM_ID]) % 100 for team_id in all_teams]

        min_team_number = min(team_number_representation)
        result = []
        for team_id, team_number in zip(all_teams, team_number_representation):
            if team_id in team_ids:
                result.append(team_number - min_team_number)

        return result
