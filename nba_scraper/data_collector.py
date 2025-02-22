import pandas as pd
from .utils import Utils
from .header_creator import HeaderCreator
import nba_scraper.configuration.schedule_and_results as sar
import nba_scraper.configuration.player_stats as ps
import nba_scraper.configuration.box_score as bs
from .configuration.global_config import DATA_FOLDER, ACTIVE_PLAYERS_FILE, ACTIVE_PLAYERS_COLUMN_NAMES
import functools
import os

WINNER = "winner=Oscar"
TEAM = "Team"


def get_nba_data_by_year_and_directory(year, directory=".", playoff=False) -> pd.DataFrame:

    csv_data_files = Utils.get_csv_files_from_directory_containing_substring(
        str(year), directory)

    return collect_data_from_csv_files(csv_data_files, directory, playoff)


def collect_data_from_csv_files(csv_files, directory="", playoff=False):
    collected_data = pd.DataFrame()

    for csv_file in csv_files:
        df = pd.read_csv(directory + csv_file)
        collected_data = pd.concat([collected_data, df])

    # Change name to own defined header
    collected_data.columns = HeaderCreator.create_schedule_and_results_header()

    collected_data[sar.DATE] = pd.to_datetime(
        collected_data[sar.DATE], format="%a, %b %d, %Y")
    collected_data = collected_data.sort_values(by=sar.DATE)

    if not playoff:
        year = csv_files[0].split("_")[0]
        collected_data = collected_data[collected_data[sar.DATE]
                                        < sar.PLAYOFF_START[year]]

    return collected_data


def _get_winner(away_team, away_points, home_team, home_points):
    if away_points > home_points:
        return away_team
    return home_team


def _get_winner_of_games(match_results_df: pd.DataFrame):
    global count_wins
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
    season_results = _count_results(match_outcomes)
    season_results = season_results.to_frame().reset_index()
    season_results.columns = [TEAM, "Games won"]
    return season_results


def get_active_players():
    active_players = pd.read_csv(DATA_FOLDER + ACTIVE_PLAYERS_FILE)
    return active_players[ACTIVE_PLAYERS_COLUMN_NAMES[0]]


def get_player_stats(player_name, directory="."):
    player_file = Utils.lowercase_non_space_file_encoding(player_name)
    return pd.read_csv(directory + player_file)


def format_name_from_file(name: str):
    parts = name.split("_")
    formatted_name = []

    for part in parts:
        if "." in part:
            part = part.upper()
        formatted_name.append(part.capitalize())

    return " ".join(formatted_name)


@functools.cache
def get_top_player_stats(statistic, season):
    csv_data_files = Utils.get_csv_files_from_directory_containing_substring(
        "", ps.DATA_DIRECTORY_PATH)

    collected_data = pd.DataFrame()

    for csv_file in csv_data_files:
        df = pd.read_csv(ps.DATA_DIRECTORY_PATH + csv_file)
        df["Player"] = format_name_from_file(csv_file.split(".")[0])

        collected_data = pd.concat([collected_data, df])

    collected_data = Utils.get_filtered_by_value(
        collected_data, "Season", season)

    return collected_data.sort_values(by=[statistic], ascending=False)


def get_box_score_for_game(game: str) -> pd.DataFrame:
    if game == None:
        # Return an empty when no game is selected
        return pd.DataFrame()

    folder_path = bs.DIRECTORY_PATH + "total_box_scores/"

    return pd.read_csv(folder_path + game)
