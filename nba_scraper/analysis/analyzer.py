import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository

import matplotlib.pyplot as plt


class Analyzer:

    def __init__(self):
        self.box_score_traditional_repository = BoxScoreTraditionalRepository()
        self.season_games_repository = SeasonGamesRepository()
        self.team_name_repository = TeamNameRepository()

    def fetch_box_score_column_data(self, team: str, season: str, *columns) -> pd.DataFrame:
        # TODO Consider adding option to directly return data as DataFrame for repo method
        result_list: list[tuple] = self.box_score_traditional_repository.fetch_box_score_by_team_and_season(
            team_id=team, season=season)
        column_names = self.box_score_traditional_repository.get_table_columns()

        result_df = pd.DataFrame(result_list, columns=column_names)

        return result_df[list(columns)]

    def fetch_season_games(self, season: str) -> pd.DataFrame:
        result_list: list[tuple] = self.season_games_repository.get_season_games(
            season=season)
        column_names = self.season_games_repository.get_table_columns()

        result_df = pd.DataFrame(result_list, columns=column_names)

        return result_df


if __name__ == "__main__":
    # TODO Extend the abstract way of picking columns to a possible wrapper function
    analyzer = Analyzer()
    # data = analyzer.fetch_box_score_column_data(
    #     "LAL", "2024-25", "game_id", "points", "assists", "total_rebounds")

    season_games = analyzer.fetch_season_games("2024-25")
    season_games.plot(kind='bar', x='date', y=[
                      'home_team_score', 'away_team_score'])

    # data.plot(kind='bar', x='game_id', y=[
    #           'points', 'assists', 'total_rebounds'])
    plt.show()
