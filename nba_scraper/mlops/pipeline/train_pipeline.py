import yaml
from mlops.data.data_loader import load_data
from mlops.data.preprocess import preprocess
from mlops.models.model_train import train_model
from mlops.models.model_eval import evaluate_model


def run_pipeline():
    config = yaml.safe_load(open("mlops/pipeline/config.yaml"))

    df = load_data()
    X_train, X_test, y_train, y_test = preprocess(df)

    model = train_model(X_train, y_train, config["model"])
    metrics = evaluate_model(model, X_test, y_test)

    print("Pipeline complete. Metrics:", metrics)


if __name__ == "__main__":
    run_pipeline()
