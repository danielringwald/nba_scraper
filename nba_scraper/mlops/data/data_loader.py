import pandas as pd
from nba_scraper.season_games.season_games_util import SeasonGamesUtil
from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository
)
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.configuration.database_config import (
    # BoxScoreTraditionalColumn as bstc,
    SeasonGamesColumn as sgc
)

WINNER_COLUMN = "winner"


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
        numeric_cols = [
            sgc.HOME_TEAM_SCORE,
            sgc.HOME_TEAM_ID,
            sgc.AWAY_TEAM_SCORE,
            sgc.AWAY_TEAM_ID
        ]

        df = SeasonGamesUtil.append_winner_column(df)

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df


if __name__ == "__main__":
    loader = DataLoader()
    season_df = loader.extract_season("2023-24")
    print(season_df.head())
