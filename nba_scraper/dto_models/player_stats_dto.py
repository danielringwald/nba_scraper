from pydantic import BaseModel, ConfigDict
from nba_scraper.db.models import PlayerStats

class PlayerStatsDto(BaseModel):

    model_config = ConfigDict(frozen=True)

    player_id: str
    game_id: str
    team_id: int

    minutes: int

    field_goals_made: int
    field_goals_attempted: int
    field_goals_percentage: int

    three_pointers_made: int
    three_pointers_attempted: int
    three_pointers_percentage: int

    free_throws_made: int
    free_throws_attempted: int
    free_throws_percentage: int

    rebounds_offensive: int
    rebounds_defensive: int
    rebounds_total: int

    assists: int
    steals: int
    blocks: int
    turnovers: int
    fouls_personal: int
    points: int
    plus_minus_points: int