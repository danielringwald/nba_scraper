import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository
)
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.configuration.database_config import (
    # BoxScoreTraditionalColumn as bstc,
    SeasonGamesColumn as sgc
)

HOME_WINNER_COLUMN = "home_team_wins"


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
        df[HOME_WINNER_COLUMN] = (df[sgc.HOME_TEAM_SCORE]
                                  > df[sgc.AWAY_TEAM_SCORE]).astype(int)

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
        home_away_prefixes = ['HOME', 'AWAY']
        df = pd.get_dummies(df, columns=team_id_cols,
                            prefix=home_away_prefixes, prefix_sep='_')

        return df


if __name__ == "__main__":
    loader = DataLoader()
    season_df = loader.extract_season("2023-24")
    feature_engineered_df = loader.feature_engineer(season_df)
    print(feature_engineered_df[HOME_WINNER_COLUMN].head())
