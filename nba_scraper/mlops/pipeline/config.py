MODEL_CONFIGS = {
    "win_model": {
        "target": "won_game",
        "features": ["avg_pts_last5", "avg_reb_last5", "win_rate_last5"],
        "model_class": "RandomForestClassifier",
        "params": {"n_estimators": 200},
        "preprocess_fn": "preprocess_for_win",
    },

    "score_model": {
        "target": "points_team",
        "features": ["avg_pts_last5", "pace_last5"],
        "model_class": "XGBRegressor",
        "params": {"max_depth": 5},
        "preprocess_fn": "preprocess_for_score",
    }
}
