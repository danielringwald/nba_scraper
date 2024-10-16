import os

class Utils:

    @staticmethod
    def get_csv_files_from_directory(directory="."):
        """Returns a list of all .csv files in the specified directory."""
        csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
        return csv_files