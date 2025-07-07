from dataclasses import dataclass
from .common_model import CommonModel
from .box_score_row import BoxScoreRow
from typing import List, Optional

@dataclass(slots=True)
class GameBoxScore(CommonModel):
    
    home_team: Optional[str]
    away_team: Optional[str]
    home_team_score: Optional[int]
    away_team_score: Optional[int]
    
    player_scores: List[BoxScoreRow]
    
    def get_player_row(self, player_name: str) -> Optional[BoxScoreRow]:
        
        if len(self.player_scores) == 0:
            return None
        
        for box_score_row in self.player_scores:
            if box_score_row.PLAYER_NAME == player_name:
                return box_score_row
            
        return None