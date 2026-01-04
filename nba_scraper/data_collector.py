import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.header_creator import HeaderCreator
import nba_scraper.configuration.schedule_and_results as sar
import nba_scraper.configuration.player_stats as ps
import nba_scraper.configuration.box_score as bs
from nba_scraper.configuration.global_config import DATA_FOLDER, ACTIVE_PLAYERS_FILE, ACTIVE_PLAYERS_COLUMN_NAMES
import functools
import xarray as xr

WINNER = "winner=Oscar"
TEAM = "Team"


@DeprecationWarning
def get_nba_data_by_year_and_directory(year, directory=".", playoff=False) -> pd.DataFrame:
    csv_data_files = Utils.get_csv_files_from_directory_containing_substring(
        str(year), directory)
    print("Data files", csv_data_files)
    return collect_data_from_csv_files(csv_data_files, directory, playoff)


def collect_data_from_csv_files(csv_files: list[str], directory="", playoff=False) -> pd.DataFrame:
    collected_data = pd.DataFrame()

    for csv_file in csv_files:
        df = pd.read_csv(directory + csv_file)
        collected_data = pd.concat([collected_data, df])

    # Change name to own defined header
    collected_data.columns = HeaderCreator.create_schedule_and_results_headers()

    collected_data[sar.DATE] = pd.to_datetime(
        collected_data[sar.DATE], format="%a, %b %d, %Y")
    collected_data = collected_data.sort_values(by=sar.DATE)

    year = csv_files[0].split("_")[0]
    if not playoff and year in sar.PLAYOFF_START.values():
        collected_data = collected_data[collected_data[sar.DATE]
                                        < sar.PLAYOFF_START[year]]

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


def get_box_scores_by_team_and_season(team: str, season: int) -> pd.DataFrame:
    """
        Gets all the games where a team has played.

        This currently counts regular season games, post-season games, in-season tournament, 
        and playoff play-in games
    """
    years_and_months_of_season = Utils._get_year_and_months_of_season(season)

    all_games_played_by_team = []
    for year_and_month in years_and_months_of_season:
        data_files_csv = Utils.get_csv_files_from_directory_containing_substring(
            bs.BOX_SCORE_DATA_FILE_TEMPLATE.format(year_and_month[0], year_and_month[1]), bs.TOTAL_BOX_SCORES_PATH)

        data_files_csv = [
            data_file for data_file in data_files_csv if "_" + team in data_file]

        if len(data_files_csv) != 0:
            all_games_played_by_team += data_files_csv

    return extract_box_score_data_from_multiple_csv_files(all_games_played_by_team, bs.TOTAL_BOX_SCORES_PATH)


def extract_box_score_data_from_multiple_csv_files(csv_files: list[str], directory: str) -> pd.DataFrame:

    games_data = []

    for csv_file in csv_files:
        game_df = extract_data_from_csv_file(csv_file, directory)

        xr_data_array = xr.DataArray(
            game_df.iloc[:, 1:].values,
            dims=("Player", "Stats"),
            coords={
                "Player": game_df.loc[:, bs.PLAYER].values,
                "Stats": game_df.columns[1:],
            }
        )

        xr_data_array.expand_dims(Game=[csv_file.removesuffix(".csv")])
        games_data.append(xr_data_array)

    return xr.concat(games_data, dim="Game")


def extract_data_from_csv_file(csv_file: str, directory: str) -> pd.DataFrame:
    return pd.read_csv(directory + csv_file)


def fetch_column_over_games(data: xr.DataArray, column: str):
    pass
