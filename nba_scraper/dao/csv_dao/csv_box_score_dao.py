import functools
from typing import List, Union
import pandas as pd
from nba_scraper.dao.csv_dao.csv_common_dao import CSVCommonDAO
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH
from nba_scraper.models.game_box_score import GameBoxScore
from nba_scraper.utils import Utils
from nba_scraper.mappers.box_score_mapper import BoxScoreMapper
from nba_scraper.dao.csv_dao.csv_dao_helper import CSVDAOHelper


class CSVBoxScoreDAO(CSVCommonDAO):

    directory = TOTAL_BOX_SCORES_PATH

    @classmethod
    @functools.lru_cache(maxsize=1000)
    def get_by_id(cls, item_id: str) -> pd.DataFrame:
        """
            Return the game box score by ID where ID is 
            on the form YYYYMMDD0<TEAM INITIALS>_<@ TEAM INITIALS>

            Args:
                season (int or list of int): A single season year or a list of season years.
                team (str): The team name.
        """
        return pd.read_csv(cls.directory + item_id + ".csv")

    @classmethod
    def get_by_team_and_season(cls, team: str, season: Union[int, List[int]]) -> List[GameBoxScore]:
        """
            Returns all games by a team during a season
        """
        seasons = Utils.to_list(season)

        game_ids = []
        for season in seasons:
            game_ids = game_ids + \
                CSVDAOHelper.get_box_score_ids_by_team_and_season(team, season)

        game_box_scores = []
        for game_id in game_ids:
            game_box_scores.append(
                BoxScoreMapper.map_df_to_box_score_game(cls.get_by_id(game_id)))

        return game_box_scores
