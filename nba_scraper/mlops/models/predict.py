import joblib
import pandas as pd

from nba_scraper.mlops.data.preprocess import Preprocess

MODEL_PATH = "artifacts/model.joblib"
PREPROCESS_PATH = "artifacts/preprocess.joblib"


def predict(features: pd.DataFrame):
    model = joblib.load(MODEL_PATH)
    preprocess = joblib.load(PREPROCESS_PATH)

    X_t = preprocess.transform(features)
    return model.predict_proba(X_t)[:, 1]
