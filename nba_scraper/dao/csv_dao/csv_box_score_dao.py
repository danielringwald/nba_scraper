<<<<<<< Updated upstream
import functools
from typing import Union
import logging
import os
import pandas as pd
from nba_scraper.dao.csv_dao.csv_common_dao import CSVCommonDAO
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH
||||||| Stash base
from .csv_common_dao import CSVCommonDAO
import pandas as pd
from utils import Utils
from typing import Union, List
=======
from typing import Union, List
from nba_scraper.dao.csv_dao.csv_common_dao import CSVCommonDAO
from nba_scraper.utils import Utils
>>>>>>> Stashed changes
from nba_scraper.models.game_box_score import GameBoxScore
<<<<<<< Updated upstream
from nba_scraper.utils import Utils
from nba_scraper.mappers.box_score_mapper import BoxScoreMapper
from nba_scraper.dao.csv_dao.csv_dao_helper import CSVDAOHelper

||||||| Stash base
from .csv_dao_helper import CSVDAOHelper
=======
import pandas as pd

>>>>>>> Stashed changes

class CSVBoxScoreDAO(CSVCommonDAO):

<<<<<<< Updated upstream
    directory = TOTAL_BOX_SCORES_PATH

    @classmethod
    @functools.lru_cache(maxsize=1000)
    def get_by_id(cls, item_id: str) -> GameBoxScore:
||||||| Stash base
    def __init__(self, directory: str):
        super().__init__(directory)
        
    def get_by_id(self, id: str) -> pd.DataFrame:
=======
    def __init__(self, directory: str):
        super().__init__(directory)

    def get_by_id(self, id: str) -> pd.DataFrame:
>>>>>>> Stashed changes
        """
<<<<<<< Updated upstream
            Return the game box score by ID where ID is 
            on the form YYYYMMDD0<TEAM INITIALS>_<@ TEAM INITIALS>

||||||| Stash base
            Return the game box score by ID where ID is on the form YYYYMMDD0<TEAM INITIALS>_<@ TEAM INITIALS>
        
=======
            Return the game box score by ID where ID is on the form YYYYMMDD0<TEAM INITIALS>_<@ TEAM INITIALS>

>>>>>>> Stashed changes
            Args:
                season (int or list of int): A single season year or a list of season years.
                team (str): The team name.

            Returns:
                pd.DataFrame: The box score data for the specified game.
        """
<<<<<<< Updated upstream
        path = os.path.join(cls.directory, item_id + ".csv")
        return BoxScoreMapper.map_df_to_box_score_game(item_id, pd.read_csv(path))

    @classmethod
    def get_by_team_and_season(cls, team: str, season: Union[int, list[int], str]) -> list[GameBoxScore]:
||||||| Stash base
        return pd.read_csv(self.directory + id + ".csv")
    
    def get_by_team_and_season(self, team: str, season: Union[int, List[int]]) -> List[GameBoxScore]:
=======
        return pd.read_csv(self.directory + id + ".csv")

    def get_by_team_and_season(self, team: str, season: Union[int, List[int]]) -> List[GameBoxScore]:
>>>>>>> Stashed changes
        """
            Returns all games by a team during a season

            Args:
                team (str): The team name.
                season (int or list of int): A single season year or a list of season years.

            Returns: 
                list[GameBoxScore]: A list of GameBoxScore objects 
                    for the specified team and season.
        """
<<<<<<< Updated upstream
        season_years = Utils.to_list(season)

        game_ids = [
            game_id
            for season_year in season_years
            for game_id in CSVDAOHelper.get_box_score_ids_by_team_and_season(team, season_year)
        ]

        game_box_scores = []
        for game_id in game_ids:
            try:
                game_box_scores.append(cls.get_by_id(game_id))
            except FileNotFoundError:
                logging.warning(
                    "Box score file not found for game ID: %s", game_id)
                continue

        return game_box_scores

    @classmethod
    def get_opposite_game(cls, game: GameBoxScore) -> GameBoxScore:
        """
            Returns the opposite game for a given game box score.

            Args:
                game (GameBoxScore): The game box score to find the opposite for.

            Returns:
                GameBoxScore: The opposite game box score.
        """

        # Expected format YYYYMMDD0<HOME TEAM>_<THIS_GAME_TEAM>
        date = game.id[:8]
        home_team = game.id[9:12]
        this_game_team = game.id[13:16]
        away_and_home_games_ids = CSVDAOHelper.get_box_score_ids_by_date_and_team(
            date, home_team)

        if len(away_and_home_games_ids) != 2:
            logging.error("Expected 2 games for %s, found %d",
                          game.id, len(away_and_home_games_ids))
            raise ValueError(
                f"Expected 2 games for {game.id}, found {len(away_and_home_games_ids)}")

        if home_team == this_game_team:
            opposite_game_id = [
                game_id
                for game_id in away_and_home_games_ids
                if home_team + "_" + home_team not in game_id]
        else:
            opposite_game_id = [
                game_id
                for game_id in away_and_home_games_ids
                if home_team + "_" + this_game_team not in game_id]

        if len(opposite_game_id) != 1:
            logging.error("Expected 1 opposite game for %s, found %d",
                          game.id, len(opposite_game_id))
            raise ValueError(
                f"Expected 1 opposite game for {game.id}, found {len(opposite_game_id)}")

        return cls.get_by_id(opposite_game_id[0])

    @classmethod
    def get_games_by_date_and_home_team(cls, date: str, home_team: str) -> list[GameBoxScore]:
        """
            Returns all games by date and home team.

            Args:
                date (str): The date in YYYYMMDD format.
                home_team (str): The home team name.

            Returns:
                list[GameBoxScore]: A list of GameBoxScore objects for the specified date and home team.
        """
        game_ids = CSVDAOHelper.get_box_score_ids_by_season(date)
        return [cls.get_by_id(game_id) for game_id in game_ids if game_id.startswith(f"{date}0{home_team}")]
||||||| Stash base
        seasons = Utils.to_list(season)
        
        Utils.get_csv_files_from_directory_and_season()
        
        return [GameBoxScore()]
=======
        seasons = Utils.to_list(season)

        Utils.get_csv_files_from_directory_and_season()

        return [GameBoxScore()]
>>>>>>> Stashed changes
