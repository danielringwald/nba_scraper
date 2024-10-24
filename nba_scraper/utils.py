import os


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

        csv_files = [file for file in os.listdir(
            directory) if Utils._has_file_ending_and_contains_substring(".csv", substring, file)]
        return csv_files

    @staticmethod
    def _has_file_ending_and_contains_substring(file_end: str, substring: str, file_name: str) -> bool:
        return file_name.endswith(file_end) and substring in file_name

    @staticmethod
    def is_file_in_directory(file: str, directory: str) -> bool:
        return file in os.listdir(directory)
