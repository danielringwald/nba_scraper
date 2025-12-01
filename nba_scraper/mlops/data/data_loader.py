import hashlib
import pandas as pd
from pathlib import Path
from typing import Iterable

from nba_scraper.dao.repository.box_score_traditional_repository import (
    BoxScoreTraditionalRepository)


class DataLoader:
    """Simple data loader for the MLOps pipeline.

    Responsibilities:
    - extract data from repository and convert to pandas.DataFrame
    - read/write parquet snapshots
    - basic feature engineering and train/validation split

    The loader is intentionally small and explicit: it does not change
    repository behaviour and is safe to use in CI / ad-hoc scripts.
    """

    def __init__(self, data_dir: str | Path = "data/ml"):
        self.repo = BoxScoreTraditionalRepository()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def extract_season(self, season: str) -> pd.DataFrame:
        """Extract season data from the repository and return a DataFrame.

        This uses the existing repository API which returns a list of tuples.
        We convert to DataFrame using column names from the repository.
        """
        rows = self.repo.fetch_all_box_scores_from_season(season=season)
        # ensure consistent empty DataFrame with correct columns
        columns = self.repo.get_table_columns()
        df = pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame(
            columns=columns)
        return df

    def save_parquet(self, df: pd.DataFrame, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)
        return path

    def load_parquet(self, path: str | Path) -> pd.DataFrame:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Parquet file not found: {path}")
        return pd.read_parquet(path)

    def feature_engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        """Small, reversible feature engineering examples.

        - fill NA for numeric columns with 0
        - ensure dtypes for a few known columns
        - keep original columns (no destructive renames)
        """
        if df.empty:
            return df

        df = df.copy()
        # normalize columns that are expected to exist
        numeric_cols = [
            "seconds_played",
            "field_goals_made",
            "field_goals_attempted",
            "three_pointers_made",
            "three_pointers_attempted",
            "free_throws_made",
            "free_throws_attempted",
            "reboundsTotal",
            "assists",
            "steals",
            "blocks",
            "turnovers",
            "foulsPersonal",
            "points",
        ]

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # example: convert starter boolean-like to int
        if "starter" in df.columns:
            df["starter"] = df["starter"].astype(int)

        return df

    def get_train_val(self, df: pd.DataFrame, features: Iterable[str], target: str, test_size: float = 0.2, random_state: int = 42):
        """Return (X_train, X_val, y_train, y_val) ready for sklearn.

        Assumes `df` already contains `features` and `target` columns.
        """
        from sklearn.model_selection import train_test_split

        if df.empty:
            raise ValueError("DataFrame is empty - nothing to split")

        X = df[list(features)]
        y = df[target]
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def fingerprint(self, df: pd.DataFrame) -> str:
        """Return a stable fingerprint for a DataFrame (not cryptographically strong).

        Uses pandas hashing of rows then an md5 of the bytes to produce a short id.
        """
        if df.empty:
            return "empty"

        # pandas.util.hash_pandas_object returns an int series per row; use values
        try:
            row_hashes = pd.util.hash_pandas_object(df, index=True).values
            m = hashlib.md5()
            m.update(row_hashes.tobytes())
            return m.hexdigest()
        except Exception:
            # fallback: use CSV serialisation (slower)
            m = hashlib.md5()
            m.update(df.to_csv(index=False).encode())
            return m.hexdigest()


def _example_usage():
    """Small demo used in local scripts or tests.

    1. Extract from repo -> DataFrame
    2. Feature engineer
    3. Save to parquet snapshot for reproducibility
    4. Get train/val splits
    """
    loader = DataLoader()
    df = loader.extract_season("2024-25")
    df = loader.feature_engineer(df)
    path = loader.save_parquet(
        df, loader.data_dir / "season=2024-25" / "train.parquet")
    print("Saved snapshot:", path)
    print("Fingerprint:", loader.fingerprint(df))


if __name__ == "__main__":
    _example_usage()
