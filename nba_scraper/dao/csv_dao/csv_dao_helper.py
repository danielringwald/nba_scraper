import functools
from typing import Union
from nba_scraper.utils import Utils
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH


class CSVDAOHelper:

    @staticmethod
    @functools.cache
    def get_box_score_ids_by_season(season: int) -> list[str]:
        csv_files = Utils.get_csv_files_from_directory_and_season(
            TOTAL_BOX_SCORES_PATH, Utils.to_list(season))
        return CSVDAOHelper._remove_suffix(csv_files, ".csv")

    @staticmethod
    @functools.cache
    def get_box_score_ids_by_team_and_season(team: str, season: Union[int, list[int]]) -> list[str]:
        csv_files = Utils.  get_csv_files_from_directory_and_season_and_team(
            TOTAL_BOX_SCORES_PATH, Utils.to_list(season), team)

        return CSVDAOHelper._remove_suffix(csv_files, ".csv")

    @staticmethod
    @functools.cache
    def get_box_score_ids_by_date_and_team(date: str, team: str) -> list[str]:
        csv_files = Utils.get_csv_files_from_directory_containing_substring(
            CSVDAOHelper._create_box_score_prefix(date, team), TOTAL_BOX_SCORES_PATH)

        return CSVDAOHelper._remove_suffix(csv_files, ".csv")

    @staticmethod
    def _remove_suffix(strs_to_remove_from: Union[str, list[str]], suffix: str) -> list[str]:
        if isinstance(strs_to_remove_from, list):
            return [str_to_update.removesuffix(suffix) for str_to_update in strs_to_remove_from]
        return [strs_to_remove_from.removesuffix(suffix)]

    @staticmethod
    def _create_box_score_prefix(date: str, team: str) -> str:
        """
            Creates a box score prefix based on the date and team.
            The format is YYYYMMDD0<HOME INITIALS>_<TEAM STATS INITIALS>
        """
        return f"{date}0{team}"
