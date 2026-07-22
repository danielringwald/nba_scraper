from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from datetime import date
import pandas as pd

class GameDto(BaseModel):

    model_config = ConfigDict(frozen=True)

    id: str
    date: date
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    winner: int

    @classmethod
    def from_box_score_traditional_row(cls, game_info: dict) -> GameDto:
        return cls(
            id=game_info["id"],
            date=game_info["date"],
            home_team_id=game_info["home_team_id"],
            away_team_id=game_info["away_team_id"],
            home_score=game_info["home_score"],
            away_score=game_info["away_score"],
            winner=game_info["winner"]
        )