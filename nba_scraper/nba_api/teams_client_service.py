from nba_api.stats.library.data import teams as NBA_TEAMS

from nba_scraper.dto_models.teams_dto import TeamDto

class TeamsClientService:

    def __init__(self):
        pass

    def fetch_all_teams(self) -> list[TeamDto]:
        team_dtos = list()
        
        for team in NBA_TEAMS:
            dto = TeamDto.from_api_list(team)
            team_dtos.append(dto)

        return team_dtos
