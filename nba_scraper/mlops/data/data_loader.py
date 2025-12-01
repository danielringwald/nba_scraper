import pandas as pd
from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository
)


class DataLoader:
    """Loads data directly from the database into DataFrames."""

    def __init__(self):
        self.repo = BoxScoreTraditionalRepository()

    def extract_season(self, season: str) -> pd.DataFrame:
        rows = self.repo.fetch_all_box_scores_from_season(season=season)
        columns = self.repo.get_table_columns()
        return pd.DataFrame(rows, columns=columns)

    def feature_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        numeric_cols = [
            "seconds_played", "field_goals_made", "field_goals_attempted",
            "three_pointers_made", "three_pointers_attempted",
            "free_throws_made", "free_throws_attempted",
            "reboundsTotal", "assists", "steals",
            "blocks", "turnovers", "foulsPersonal", "points"
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df
