from nba_scraper.db.session import SessionLocal
from nba_scraper.nba_api.teams_client_service import TeamsClientService
from nba_scraper.repository.team_repository import TeamRepository
from nba_scraper.mappers.teams_dto_mapper import TeamMapper

with SessionLocal() as session:
    team_client = TeamsClientService()
    team_repo = TeamRepository(session)

    teams = team_client.fetch_all_teams()

    team = team_repo.get_by_team_abbreviation("ATL")
    print(team)
