from dataclasses import dataclass

@dataclass(slots=True)
class BoxScoreRow:
    
    starter: bool
    
    PLAYER_NAME: str
    MP: str
    FG: int
    FGA: int
    FG_PERCENTAGE: float
    THREE_POINTERS_MADE: int
    THREE_POINTERS_ATTEMPTED: int
    THREE_POINTERS_PERCENTAGE: float
    FT: int
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
