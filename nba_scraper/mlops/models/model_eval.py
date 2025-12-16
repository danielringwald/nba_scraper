from sklearn.metrics import accuracy_score, roc_auc_score


def evaluate(model, preprocess, X, y):
    X_t = preprocess.transform(X)
    preds = model.predict(X_t)
    probs = model.predict_proba(X_t)[:, 1]

    return {
        "accuracy": accuracy_score(y, preds),
        "roc_auc": roc_auc_score(y, probs),
    }
