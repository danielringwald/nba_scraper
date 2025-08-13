from .csv_common_dao import CSVCommonDAO
import pandas as pd
from nba_scraper.utils import Utils
from typing import Union, List
from nba_scraper.models.game_box_score import GameBoxScore
from .csv_dao_helper import CSVDAOHelper
from ...mappers.box_score_mapper import BoxScoreMapper
import functools

class CSVBoxScoreDAO(CSVCommonDAO):

    def __init__(self, directory: str):
        super().__init__(directory)
        
    
    def get_by_id(self, id: str) -> pd.DataFrame:
        """
            Return the game box score by ID where ID is on the form YYYYMMDD0<TEAM INITIALS>_<@ TEAM INITIALS>
        
            Args:
                season (int or list of int): A single season year or a list of season years.
                team (str): The team name.
        """
        return pd.read_csv(self.directory + id + ".csv")
    
    def get_by_team_and_season(self, team: str, season: Union[int, List[int]]) -> List[GameBoxScore]:
        """
            Returns all games by a team during a season
        """
        seasons = Utils.to_list(season)
        
        game_ids = []
        for season in seasons:
            game_ids = game_ids + CSVDAOHelper.get_box_score_ids_by_team_and_season(team, season)
        
        game_box_scores = []
        for game_id in game_ids:
            game_box_scores.append(BoxScoreMapper.map_df_to_box_score_game(self.get_by_id(game_id)))
        
        return game_box_scores
