import pandas as pd
from nba_scraper.utils import Utils
from nba_scraper.configuration.database_config import SeasonGamesColumn as sgc

WINNER_COLUMN = "winner"


class SeasonGamesUtil:

    @staticmethod
    def append_winner_column(season_games: dict[str, str] | list[dict[str, str]], team_id: str = None) -> list[dict[str, str]]:
        """
            Append a 'winner' column to the season games data, indicating the winning team_id

            If team_id is provided, the 'winner' column will be 1 if the specified team won, else 0
            If team_id is NOT provided, the 'winner' column will contain the winning team_id
        """

        season_games = Utils.to_list(season_games)

        if team_id:
            for game in season_games:
                home_score = game[sgc.HOME_TEAM_SCORE]
                away_score = game[sgc.AWAY_TEAM_SCORE]

                if home_score > away_score:
                    if game[sgc.HOME_TEAM_ID] == team_id:
                        game[WINNER_COLUMN] = 1
                    else:
                        game[WINNER_COLUMN] = 0
                else:
                    if game[sgc.AWAY_TEAM_ID] == team_id:
                        game[WINNER_COLUMN] = 1
                    else:
                        game[WINNER_COLUMN] = 0
            return season_games

        for game in season_games:
            if game[sgc.HOME_TEAM_SCORE] > game[sgc.AWAY_TEAM_SCORE]:
                game[WINNER_COLUMN] = game[sgc.HOME_TEAM_ID]
            else:
                game[WINNER_COLUMN] = game[sgc.AWAY_TEAM_ID]
        return season_games
