from .csv_common_dao import CSVCommonDAO
import pandas as pd

class CSVBoxScoreDAO(CSVCommonDAO):

    def __init__(self, directory: str):
        super().__init__(directory)
        
    def get_by_id(self, id: str) -> pd.DataFrame:
        return pd.read_csv(self.directory + id + ".csv")