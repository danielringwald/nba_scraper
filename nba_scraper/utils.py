import os
import functools
import logging
from typing import Union, Sequence, TypeVar
import pandas as pd
from nba_scraper.configuration.global_config import SEASON_MONTHS, CORONA_SEASON_MONTHS, MONTH_NAME_TO_NUMBER

BOX_SCORE_DATA_FILE_TEMPLATE = "{}{}"

T = TypeVar("T")


class Utils:

    @staticmethod
    def get_csv_files_from_directory(directory="."):
        """Returns a list of all .csv files in the specified directory."""
        csv_files = [file for file in os.listdir(
            directory) if file.endswith('.csv')]
        return csv_files

    @staticmethod
    @functools.lru_cache(maxsize=1000)
    def get_csv_files_from_directory_containing_substring(substring: str, directory=".") -> list[str]:
        """Returns a list of all .csv files in the specified directory that contain {substring}."""

        try:
            directory_file_list = os.listdir(directory)
        except FileNotFoundError as exc:
            logging.error("Directory %s not found.", directory)
            raise FileNotFoundError(
                f"Directory {directory} not found.") from exc

        csv_files = [file for file in directory_file_list if Utils._has_file_ending_and_contains_substring(
            ".csv", substring, file)]

        return csv_files

    @staticmethod
    def _has_file_ending_and_contains_substring(file_end: str, substring: str, file_name: str) -> bool:
        return file_name.endswith(file_end) and substring in file_name

    @staticmethod
    def is_file_in_directory(file: str, directory: str) -> bool:

        if not os.path.isdir(directory):
            return False

        return file in os.listdir(directory)

    @staticmethod
    def convert_list_using_dictionary(list_to_convert: list, dictionary: dict):
        converted_list = [dictionary[entry] for entry in list_to_convert]
        return converted_list

    @staticmethod
    def lowercase_non_space_file_encoding(file_name, file_ending=".csv"):
        return str(file_name).lower().replace(" ", "_") + file_ending

    @staticmethod
    def get_filtered_by_value(df, column, value) -> pd.DataFrame:
        return df[df[column] == value]

    @staticmethod
    def choose_season_months(year: str) -> list[str]:
        """
            Function to choose which months to scrape. This is because of corona season where the season was irregular.
        """
        if year == "2020" or year == "2021":
            return CORONA_SEASON_MONTHS[year]
        return SEASON_MONTHS

    @staticmethod
    def get_csv_files_from_directory_and_season(directory: str, seasons: list[int]) -> list[str]:
        # TODO use get_csv_files_from_directory or write a similar implementation where we use the _get_year_and_months_of_season to know which IDs we want
        seasons = Utils.to_list(seasons)
        csv_file_list = []
        for season in seasons:
            year_and_months_of_season: list[tuple[int, int]] = Utils._get_year_and_months_of_season(
                season=season)
            for year, month in year_and_months_of_season:
                csv_file_list = csv_file_list + \
                    Utils.get_csv_files_from_directory_containing_substring(
                        str(year) + Utils._convert_to_month_number_as_str(month=month), directory)

        return csv_file_list

    @staticmethod
    def get_csv_files_from_directory_and_season_and_team(directory: str, seasons: list[int], team: str) -> list[str]:
        csv_files_from_season = Utils.get_csv_files_from_directory_and_season(
            directory, seasons)

        home_game_prefixes = [
            csv_file.split("_")[0] for csv_file in csv_files_from_season if team + "_" + team in csv_file]
        away_game_prefixes = [
            csv_file.split("_")[0] for csv_file in csv_files_from_season
            if team in csv_file and not (team + "_") in csv_file]

        return [csv_file for csv_file in csv_files_from_season if csv_file[:12] in (home_game_prefixes + away_game_prefixes)]

    @staticmethod
    def _get_year_and_months_of_season(season: int) -> list[tuple[int, int]]:
        """
            Contains data in a list with tuples that are the different months and years

            e.g. [(2025, 10), (2025, 11), (2025, 12), (2026, 1)]
        """
        months_of_season = Utils.choose_season_months(str(season))

        month_numbers_and_years = []
        current_months_season = season - 1
        for month in months_of_season:
            month_number = Utils._convert_month_name_to_month_number(month)
            if month_number == MONTH_NAME_TO_NUMBER["JANUARY"]:
                current_months_season += 1

            month_numbers_and_years.append(
                (int(current_months_season), int(month_number)))

        return month_numbers_and_years

    @staticmethod
    def _convert_month_name_to_month_number(month: str) -> str:
        return MONTH_NAME_TO_NUMBER[month.upper()]

    @staticmethod
    def _convert_to_month_number_as_str(month: int) -> str:
        return f"0{month}" if month < 10 else str(month)

    @staticmethod
    def to_list(val: Union[T, list[T]]) -> list[T]:

        if isinstance(val, list):
            return list(val)
        return [val]

    @staticmethod
    def extract_data_from_csv_file(csv_file: str, directory: str) -> pd.DataFrame:
        return pd.read_csv(directory + csv_file)

    @staticmethod
    def get_game_id_prefix(box_score_id: str) -> str:
        """
            Extracts the prefix from a box score ID.
            The prefix is the first 12 characters of the ID.
        """
        return box_score_id[:12]

    @staticmethod
    def get_home_team(box_score_id: str) -> str:
        """
            Extracts the home team initials from a box score ID.
            The home team initials are the characters at positions 9 to 12.
        """
        return box_score_id[9:12]

    @staticmethod
    def get_stat_team(box_score_id: str) -> str:
        """
            Extracts the suffix from a box score ID.
            The suffix is the last 3 characters of the ID.
        """
        return box_score_id[-3:]

    @staticmethod
    def get_game_date(box_score_id: str) -> str:
        """
            Extracts the game date from a box score ID.
            The date is the first 8 characters of the ID.
        """
        return box_score_id[:8]
