from sqlalchemy.orm import Session
from sqlalchemy import select
from nba_scraper.db.models import Team

class TeamRepository():

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, team_id: int) -> Team:
        return self.session.get(Team, team_id)
    
    def get_by_team_abbreviation(self, team_abbreviation: str) -> Team:
        statement = select(Team).where(Team.abbreviation == team_abbreviation)

        # one_or_none() fails if there are more than 1 teams returned
        return self.session.scalars(statement).one_or_none()

    def get_by_team_name(self, team_name: str) -> Team:
        statement = select(Team).where(Team.name == team_name)

        return self.session.scalars(statement).one_or_none()
    
    def save(self, team: Team):
        self.session.add(team)
        print(f"Successfully added team {team} to DB")

    def save_all(self, teams: list[Team]):
        self.session.add_all(teams)