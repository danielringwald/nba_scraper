from __future__ import annotations

from pydantic import BaseModel, ConfigDict

class TeamDto(BaseModel):

    model_config = ConfigDict(frozen=True)

    team_id: int
    team_abbreviation: str
    city: str
    name: str

    @classmethod
    def from_api_list(cls, team_list: list) -> TeamDto:
        return cls(
            team_id=team_list[0],
            team_abbreviation=team_list[1],
            city=team_list[4],
            name=team_list[5],
        )