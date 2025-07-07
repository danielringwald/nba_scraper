from abc import abstractmethod
from ..common_dao import CommonDAO

class CSVCommonDAO(CommonDAO):

    def __init__(self, directory: str):
        self.directory = directory
        
    