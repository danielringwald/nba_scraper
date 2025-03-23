from utils import Utils
import nba_scraper.configuration.box_score as bs
import matplotlib.pyplot as plt


class Analyzer:

    def rebounds_against_wins():
        # Count the number of rebounds and see how many wins
        pass

    def collect_games_data():
        box_score_dir = bs.DIRECTORY_PATH
        total_box_score_dir = box_score_dir + "total_box_scores"
        Utils.get_csv_files_from_directory_containing_substring(
            "", directory=total_box_score_dir)

        pass

    def find_games_substrings(season):
        uppercase_months = list(
            map(str.upper, Utils.choose_season_months(season)))
