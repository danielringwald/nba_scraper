from abc import ABC

MODEL_CONFIGS = {
    "last_n_games_random_forest": {
        "target": "won_game",
        "features": ["avg_pts_last5", "avg_reb_last5", "win_rate_last5"],
        "data_loader_method_name": "load_last_n_games_dataset",
        "model_class": "RandomForestClassifier",
        "model_params": {"n_estimators": 200},
        "preprocess_fn": "preprocess_for_win",
    },

    "score_model": {
        "target": "points_team",
        "features": ["avg_pts_last5", "pace_last5"],
        "model_class": "XGBRegressor",
        "model_params": {"max_depth": 5},
        "preprocess_fn": "preprocess_for_score",
    },
    
    "xgboost_20_features": {
        "target": "won_game",
        "data_loader_method_name": "load_xgboost_20_features_dataset",
        "model_class": "XGBRegressor",
        "model_params": {"max_depth": 5},
        "preprocessor_fn": 
    }
}

class CommonFeatures(ABC):

    GAME_ID = "game_id"
    DATE = "date"
    
class LastNGamesFeatures(CommonFeatures):

    WINNER = "winner"

    DATE_DAY = "day"
    DATE_MONTH = "month"
    DATE_YEAR = "year"

    HOME_TEAM = None # "home_team", Boolean field, not implemented yet
    AWAY_TEAM = None # "away_team", Boolean field, not implemented yet

    NTH_GAME_PREFIX = "WON_LAST_GAME_"
    """ Should be like "WON_LAST_GAME_X" where X is the number"""

    ROLLING_WIN_RATE = "rolling_win_rate"

class PointDiffFeatures(CommonFeatures):
    
    POINT_DIFF = "point_diff"
    POINTS_SCORED = "points_scored"
    POINTS_ALLOWED = "points_allowed"
    
    IS_HOME = "is_home" 
    TEAM_ABBREVIATION = "team_abbreviation"
    
    AVG_POINT_DIFF_LAST_N = "avg_point_diff_last_n"
    AVG_POINTS_SCORED_LAST_N = "avg_points_scored_last_n"
    AVG_POINTS_ALLOWED_LAST_N = "avg_points_allowed_last_n"
    DAYS_SINCE_LAST_GAME = "days_since_last_game"
    IS_BACK_TO_BACK = "is_back_to_back"