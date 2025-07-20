from .csv_common_dao import CSVCommonDAO
import pandas as pd
from utils import Utils
from typing import Union, List
from nba_scraper.models.game_box_score import GameBoxScore
from .csv_dao_helper import CSVDAOHelper

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
        
        Utils.get_csv_files_from_directory_and_season()
        
        return [GameBoxScore()]