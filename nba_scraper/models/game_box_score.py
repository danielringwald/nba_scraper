from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from nba_scraper.models.common_model import CommonModel
from nba_scraper.models.box_score_row import BoxScoreRow


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

    def get_sum_of_column(self, column_name: str) -> int:
        """
            Returns the sum of a specific column across all player scores.
        """

        if isinstance(column_name, Enum):
            column_name = column_name.value

        return sum(getattr(row, column_name) for row in self.player_scores)
