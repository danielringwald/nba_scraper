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


class LastNGamesFeatures:

    WINNER = "winner"

    DATE_DAY = "day"
    DATE_MONTH = "month"
    DATE_YEAR = "year"

    HOME_TEAM = "home_team"  # Boolean field
    AWAY_TEAM = "away_team"  # Boolean field

    NTH_GAME_PREFIX = "WON_LAST_GAME_"
    """ Should be like "WON_LAST_GAME_X" where X is the number"""

    ROLLING_WIN_RATE = "rolling_win_rate"
