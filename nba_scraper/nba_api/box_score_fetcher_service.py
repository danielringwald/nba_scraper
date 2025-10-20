import regex as re
from nba_api.stats.endpoints import boxscoretraditionalv3
from nba_api.stats.library.data import teams


class BoxScoreFetcherService:
    """
        This service is possibly unnecessary
    """

    def fetch_box_score_from_game_id(self, game_id: str):
        box_score = boxscoretraditionalv3.BoxScoreTraditionalV3(
            game_id=game_id)
        return box_score.get_data_frames()
