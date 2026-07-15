from nba_scraper.db.models import Team
from nba_scraper.dto_models.teams_dto import TeamDto

class TeamMapper:

    @staticmethod
    def to_db_model(team_dto: TeamDto) -> Team:
        return Team(
            id=team_dto.team_id,
            abbreviation=team_dto.team_abbreviation,
            city=team_dto.city,
            name=team_dto.name
        )