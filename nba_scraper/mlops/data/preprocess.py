import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from nba_scraper.mlops.pipeline.config import LastNGamesFeatures as lngf
from nba_scraper.mlops.utils.helpers import LastNGamesHelper


class Preprocess:

    def __init__(self):
        self.column_transformer: ColumnTransformer | None = None
        self.numeric_features: list[str] | None = None
        self.binary_features: list[str] | None = None

    # ---------- schema / setup ----------

    def _infer_feature_groups(self, features: pd.DataFrame):
        self.numeric_features = [
            lngf.DATE_DAY,
            lngf.DATE_MONTH,
            lngf.DATE_YEAR,
            lngf.ROLLING_WIN_RATE,
        ]

        self.binary_features = [] + LastNGamesHelper.filter_nth_game_features(
            features.columns
        )

    def _build_column_transformer(self, numeric_scaler_cls = StandardScaler):
        self.column_transformer = ColumnTransformer(
            transformers=[
                ("num", "passthrough", self.numeric_features),
                ("bin", "passthrough", self.binary_features),
            ],
            remainder="drop"
        )

    # ---------- public API ----------

    def fit(self, features: pd.DataFrame):
        self._infer_feature_groups(features)
        self._build_column_transformer()
        self.column_transformer.fit(features)
        return self

    def transform(self, features: pd.DataFrame):
        if self.column_transformer is None:
            raise RuntimeError("Preprocess must be fitted before calling transform()")

        return self.column_transformer.transform(features)

    def fit_transform(self, features: pd.DataFrame):
        self.fit(features)
        return self.transform(features)
