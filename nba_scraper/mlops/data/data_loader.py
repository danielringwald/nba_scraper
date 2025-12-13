import datetime
import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository
)
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.configuration.database_config import (
    # BoxScoreTraditionalColumn as bstc,
    SeasonGamesColumn as sgc
)
from nba_scraper.mlops.pipeline.config import LastNGamesFeatures as lngf

HOME_WINNER_COLUMN = "home_team_wins"
HOME_AWAY_PREFIXES = ['HOME', 'AWAY']


class DataLoader:
    """Loads data directly from the database into DataFrames."""

    def __init__(self):
        self.box_score_traditional_repo = BoxScoreTraditionalRepository()
        self.season_games_repo = SeasonGamesRepository()

    def extract_season(self, season: str) -> pd.DataFrame:
        rows = self.season_games_repo.get_season_games(season=season)
        return pd.DataFrame(rows)

    def feature_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # 1. Append winner column
        df = self._append_season_game_home_winner_df(df)

        # 2. Clean numeric columns
        numeric_cols = [
            sgc.HOME_TEAM_SCORE,
            sgc.AWAY_TEAM_SCORE
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # 3. One-hot encode the away and home teams
        team_id_cols = [sgc.HOME_TEAM_ABBREVIATION, sgc.AWAY_TEAM_ABBREVIATION]
        df = pd.get_dummies(df, columns=team_id_cols,
                            prefix=HOME_AWAY_PREFIXES, prefix_sep='_')

        return df

    def feature_engineer_last_n_winner(self, df: pd.DataFrame, n_games: int = 5) -> pd.DataFrame:
        df = df.copy()

        # 1. Append winner column
        df = self._append_season_game_home_winner_df(df)

        # 2. For all teams, for each last n_games games, check the outcome of the next
        team_abbreviation = "CLE"

        sub_df = df.loc[
            (df[sgc.HOME_TEAM_ABBREVIATION] == team_abbreviation) | (
                df[sgc.AWAY_TEAM_ABBREVIATION] == team_abbreviation)
        ].sort_values(sgc.DATE, ascending=True)

        for i in range(n_games, len(sub_df)):
            current_game = sub_df.iloc[n_games]
            last_n_games = sub_df.iloc[i - n_games: n_games]

            print(current_game)
            print(last_n_games[[sgc.DATE, sgc.HOME_TEAM_ABBREVIATION,
                  sgc.HOME_TEAM_SCORE, sgc.AWAY_TEAM_ABBREVIATION, sgc.AWAY_TEAM_SCORE]])

            row = {}
            row[lngf.WINNER] = int((current_game[HOME_WINNER_COLUMN] == 1 and current_game[sgc.HOME_TEAM_ABBREVIATION] == team_abbreviation) or
                                   (current_game[HOME_WINNER_COLUMN] == 0 and current_game[sgc.AWAY_TEAM_ABBREVIATION] == team_abbreviation))
            row[lngf.DATE_DAY] = datetime.date.fromisoformat(
                str(current_game[sgc.DATE])).day
            row[lngf.DATE_MONTH] = datetime.date.fromisoformat(
                str(current_game[sgc.DATE])).month
            row[lngf.DATE_YEAR] = datetime.date.fromisoformat(
                str(current_game[sgc.DATE])).year

            for i in range(n_games):
                n_game = last_n_games.iloc[n_games - i - 1]
                row[lngf.NTH_GAME_PREFIX + str(i + 1)] = int((n_game[HOME_WINNER_COLUMN] == 1 and n_game[sgc.HOME_TEAM_ABBREVIATION] == team_abbreviation) or
                                                             (n_game[HOME_WINNER_COLUMN] == 0 and n_game[sgc.AWAY_TEAM_ABBREVIATION] == team_abbreviation))

            print(pd.DataFrame(row, index=[
                  team_abbreviation + str(current_game[sgc.DATE])]))
            return pd.DataFrame()

        return df

    def _append_season_game_home_winner_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[HOME_WINNER_COLUMN] = (df[sgc.HOME_TEAM_SCORE]
                                  > df[sgc.AWAY_TEAM_SCORE]).astype(int)

        return df


if __name__ == "__main__":
    loader = DataLoader()
    season_df = loader.extract_season("2025-26")
    feature_engineered_df = loader.feature_engineer_last_n_winner(season_df)
    # print(feature_engineered_df[HOME_WINNER_COLUMN].head())
