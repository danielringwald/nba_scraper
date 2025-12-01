import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier


def train_model(X_train, y_train, params):
    with mlflow.start_run():
        mlflow.log_params(params)

        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        mlflow.sklearn.log_model(model, "model")

        return model
