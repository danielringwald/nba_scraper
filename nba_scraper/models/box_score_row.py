from dataclasses import dataclass, fields
from enum import Enum


@dataclass(slots=True)
class BoxScoreRow:

    IS_STARTER: bool

    PLAYER_NAME: str
    MP: str
    FG: int  # Number of Field Goals Made
    FGA: int
    FG_PERCENTAGE: float
    THREE_POINTERS_MADE: int
    THREE_POINTERS_ATTEMPTED: int
    THREE_POINTERS_PERCENTAGE: float
    FT: int  # Number of Free Throws Made
    FTA: int
    FT_PERCENTAGE: float
    ORB: int
    DRB: int
    TRB: int
    AST: int
    STL: int
    BLK: int
    TOV: int
    PF: int
    PTS: int
    GAME_SCORE: float
    PLUS_MINUS: int


BoxScoreRow.Fields = Enum(
    "Fields",
    {f.name: f.name for f in fields(BoxScoreRow)}
)
