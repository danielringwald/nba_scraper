from nba_scraper.db.models import Game
from nba_scraper.dto_models.games_dto import GameDto

class GameMapper:

    @staticmethod
    def to_db_model(game_dto: GameDto) -> Game:
        return Game(
            id=game_dto["id"],
            date=game_dto["date"],
            home_team_id=game_dto["home_team_id"],
            away_team_id=game_dto["away_team_id"],
            home_score=game_dto["home_score"],
            away_score=game_dto["away_score"],
            winner=game_dto["winner"]
        )