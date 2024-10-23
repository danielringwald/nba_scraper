import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import Utils
from header_creator import HeaderCreator
import nba_scraper.configuration.schedule_and_results as sar


WINNER = "winner"


def get_nba_data_by_year_and_directory(year, directory=".") -> pd.DataFrame:
    collected_dataframe = pd.DataFrame()

    csv_data_files = Utils.get_csv_files_from_directory_containing_substring(
        str(year), directory)

    return collect_data_from_csv_files(csv_data_files, directory)


def collect_data_from_csv_files(csv_files, directory=""):
    collected_data = pd.DataFrame()

    for csv_file in csv_files:
        df = pd.read_csv(directory + csv_file)
        collected_data = pd.concat([collected_data, df])

    # Change name to own defined header
    collected_data.columns = HeaderCreator.create_schedule_and_results_header()
    return collected_data


def _get_winner(away_team, away_points, home_team, home_points):
    if away_points > home_points:
        return away_team
    return home_team


def _get_winner_of_games(match_results_df: pd.DataFrame):
    results = pd.DataFrame()

    results[[sar.AWAY_TEAM, sar.AWAY_TEAM_POINTS, sar.HOME_TEAM,
             sar.HOME_TEAM_POINTS]] = match_results_df[[sar.AWAY_TEAM, sar.AWAY_TEAM_POINTS, sar.HOME_TEAM,
                                                        sar.HOME_TEAM_POINTS]]

    results[WINNER] = results.apply(lambda game: _get_winner(
        game[sar.AWAY_TEAM], game[sar.AWAY_TEAM_POINTS], game[sar.HOME_TEAM], game[sar.HOME_TEAM_POINTS]), axis=1)

    return results


def _count_results(match_results_df: pd.DataFrame):
    return match_results_df.value_counts(WINNER)


def get_total_results_by_team(match_results_df: pd.DataFrame):
    match_outcomes = _get_winner_of_games(match_results_df)

    return _count_results(match_outcomes)
