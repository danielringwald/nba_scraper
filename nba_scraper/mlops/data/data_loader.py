import logging
import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository
)
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.team_name_repository import TeamNameRepository
from nba_scraper.configuration.database_config import (
    # BoxScoreTraditionalColumn as bstc,
    SeasonGamesColumn as sgc,
    TeamInformationColumn as tic
)
from nba_scraper.mlops.pipeline.config import LastNGamesFeatures as lngf

from nba_scraper.configuration.logging_config import init_logging
init_logging()
logger = logging.getLogger(__name__)

HOME_WINNER_COLUMN = "home_team_wins"
HOME_AWAY_PREFIXES = ['HOME', 'AWAY']


class DataLoader:
    """Loads data directly from the database into DataFrames."""

    def __init__(self):
        self.box_score_traditional_repo = BoxScoreTraditionalRepository()
        self.season_games_repo = SeasonGamesRepository()
        self.team_name_repo = TeamNameRepository()

    def extract_season(self, season: str) -> pd.DataFrame:
        rows = self.season_games_repo.get_season_games(season=season)
        return pd.DataFrame(rows)

    def feature_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        """df = df.copy()

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

        return df"""
        raise NotImplementedError("feature_engineering() is not yet implemented")

    def _feature_engineer_last_n_winner(self, input_df: pd.DataFrame, input_n_games: int = 5) -> pd.DataFrame:
        df: pd.DataFrame = input_df.copy()

        # 1. Append winner column
        df = self._append_season_game_home_winner_df(df)
        logger.info("Winner column appended")

        # 2. For all teams, for each last n_games games, check the outcome of the next
        dict_rows_for_df = []

        for team_name_information in self.team_name_repo.get_all_teams_information():
            team_abbreviation = team_name_information[tic.TEAM_ABBREVIATION]
            logger.debug("Processing team: %s", team_abbreviation)

            sub_df: pd.DataFrame = df.loc[
                (df[sgc.HOME_TEAM_ABBREVIATION] == team_abbreviation) | (
                    df[sgc.AWAY_TEAM_ABBREVIATION] == team_abbreviation)
            ].sort_values(sgc.DATE, ascending=True)

            n_games = min(input_n_games, len(sub_df) - 1)

            for game_idx in range(n_games, len(sub_df)):

                # This will be the game to predict
                current_game = sub_df.iloc[game_idx]
                # These are the last n games played
                last_n_games = sub_df.iloc[game_idx - n_games: game_idx]

                row = {}
                row[lngf.WINNER] = self._if_team_is_winner(
                    current_game, team_abbreviation)

                date: pd.Timestamp = pd.to_datetime(current_game[sgc.DATE])
                row[lngf.DATE_DAY] = date.day
                row[lngf.DATE_MONTH] = date.month
                row[lngf.DATE_YEAR] = date.year

                for game_offset in range(n_games):
                    n_game = last_n_games.iloc[n_games - game_offset - 1]
                    row[lngf.NTH_GAME_PREFIX +
                        str(game_offset + 1)] = self._if_team_is_winner(n_game, team_abbreviation)

                wins = [
                    self._if_team_is_winner(game, team_abbreviation)
                    for _, game in last_n_games.iterrows()
                ]
                row[lngf.ROLLING_WIN_RATE] = sum(wins) / n_games

                dict_rows_for_df.append(row)

        logger.info("Feature engineering for last %d games completed", n_games)

        return pd.DataFrame(dict_rows_for_df)
    
    def load_last_n_games_dataset(
        self,
        season: str,
        n_games: int = 5,
        target_col: str = lngf.WINNER,
    ) -> tuple[pd.DataFrame, pd.Series]:

        df = self.extract_season(season)
        df = self._feature_engineer_last_n_winner(df, input_n_games=n_games)

        features = df.drop(columns=[target_col])
        targets = df[target_col]

        return features, targets


    def _append_season_game_home_winner_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df[HOME_WINNER_COLUMN] = (df[sgc.HOME_TEAM_SCORE]
                                  > df[sgc.AWAY_TEAM_SCORE]).astype(int)
        return df

    def _if_team_is_winner(self, game: pd.Series, team_abbreviation: str) -> int:
        if game[sgc.HOME_TEAM_ABBREVIATION] == team_abbreviation:
            return int(game[HOME_WINNER_COLUMN] == 1)
        return int(game[HOME_WINNER_COLUMN] == 0)

    def _get_number_of_wins(self, row: dict) -> int:
        get_winner_keys = [
            key for key in row.keys() if key.startswith(lngf.NTH_GAME_PREFIX)
        ]
        return sum(row[key] for key in get_winner_keys)


if __name__ == "__main__":
    loader = DataLoader()
    season_df = loader.extract_season("2025-26")
    feature_engineered_df = loader._feature_engineer_last_n_winner(season_df)
    logger.info(feature_engineered_df.head())
