import functools
from utils import Utils
from configuration.box_score import TOTAL_BOX_SCORES_PATH

class CSVDAOHelper:
    
    @staticmethod
    @functools.cache
    def get_box_score_ids_by_season(season: int):
        Utils.get_csv_files_from_directory_and_season(TOTAL_BOX_SCORES_PATH, season)