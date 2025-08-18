from nba_scraper.dao.common_dao import CommonDAO


class CSVCommonDAO(CommonDAO):

    def __init__(self, directory: str):
        self.directory = directory
