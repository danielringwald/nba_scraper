import os
from pathlib import Path
import joblib
import logging

from nba_scraper.mlops.data.data_loader import DataLoader
from nba_scraper.mlops.data.preprocess import Preprocess
from nba_scraper.mlops.models.model_eval import evaluate
from nba_scraper.mlops.models.model import MODEL_REGISTRY
from nba_scraper.mlops.pipeline.config import MODEL_CONFIGS

from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

ARTIFACT_DIR = Path(os.path.join(os.path.dirname(__file__), "..", "results/artifacts"))
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
PREPROCESS_PATH = ARTIFACT_DIR / "preprocess.joblib"

def run(
    season: str = "2025-26",
    model_name: str = "last_n_games_random_forest",
    n_games: int = 4,
    test_size: float = 0.2,
    random_state: int = 42,
):
    # 0. Create dir if does not exist
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load dataset
    loader = DataLoader()
    # TODO abstract away data_loader method to model configs
    X, y = loader.load_last_n_games_dataset(season, n_games)

    # 2. Split
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    # 3. Preprocess
    preprocess = Preprocess()
    X_train_t = preprocess.fit_transform(X_train)

    # 4. Train model
    model_config = MODEL_CONFIGS[model_name]
    model = MODEL_REGISTRY[model_config["model_class"]](model_config["model_params"])
    model.fit(X_train_t, y_train)

    # 5. Evaluate
    metrics = evaluate(model, preprocess, X_val, y_val)

    # 6. Persist artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocess, PREPROCESS_PATH)
    joblib.dump(model_config, ARTIFACT_DIR / "model_config.joblib")

    logger.info("Training pipeline completed")
    logger.info("Metrics: %s", metrics)


if __name__ == "__main__":
    run()
