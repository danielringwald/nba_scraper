import joblib
from sklearn.model_selection import train_test_split

from nba_scraper.mlops.data.data_loader import DataLoader
from nba_scraper.mlops.data.preprocess import Preprocess
from nba_scraper.mlops.models.model import build_model


MODEL_PATH = "artifacts/model.joblib"
PREPROCESS_PATH = "artifacts/preprocess.joblib"


def train(season: str = "2025-26", n_games: int = 5):
    # 1. Load dataset
    loader = DataLoader()
    X, y = loader.load_last_n_games_dataset(season, n_games)

    # 2. Split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Preprocess
    preprocess = Preprocess()
    X_train_t = preprocess.fit_transform(X_train)
    X_val_t = preprocess.transform(X_val)

    # 4. Train model
    model = build_model()
    model.fit(X_train_t, y_train)

    # 5. Persist artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(preprocess, PREPROCESS_PATH)

    print("Training complete")


if __name__ == "__main__":
    train()
