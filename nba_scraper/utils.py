import os
import pandas as pd
from nba_scraper.configuration.global_config import SEASON_MONTHS, CORONA_SEASON_MONTHS, MONTH_NAME_TO_NUMBER

BOX_SCORE_DATA_FILE_TEMPLATE = "{}{}"


class Utils:

    @staticmethod
    def get_csv_files_from_directory(directory="."):
        """Returns a list of all .csv files in the specified directory."""
        csv_files = [file for file in os.listdir(
            directory) if file.endswith('.csv')]
        return csv_files

    @staticmethod
    def get_csv_files_from_directory_containing_substring(substring: str, directory=".") -> list[str]:
        """Returns a list of all .csv files in the specified directory that contain {substring}."""

        try:
            directory_file_list = os.listdir(directory)
        except FileNotFoundError:
            print(f"Directory {directory} not found.")
            raise FileNotFoundError(f"Directory {directory} not found.")

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
    def get_csv_files_from_directory_and_season(directory: str, season: int) -> list[str]:
        return

    @staticmethod
    def _get_year_and_months_of_season(season: int) -> list[tuple[str, str]]:
        months_of_season = Utils.choose_season_months(str(season))

        month_numbers_and_years = []
        current_months_season = season - 1
        for month in months_of_season:
            month_number = Utils._convert_month_name_to_month_number(month)
            if month_number == MONTH_NAME_TO_NUMBER["JANUARY"]:
                current_months_season += 1

            month_numbers_and_years.append(
                (str(current_months_season), month_number))

        return month_numbers_and_years

    @staticmethod
    def _convert_month_name_to_month_number(month: str) -> str:
        return MONTH_NAME_TO_NUMBER[month.upper()]
