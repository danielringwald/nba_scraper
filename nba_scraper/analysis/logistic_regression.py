import pandas as pd
import numpy as np
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository


class LogisticRegressionAnalyzer:

    GRADIENT_DESCENT_ITERATIONS = 10000
    LEARNING_RATE = 0.001

    def __init__(self):
        self.season_games_repository = SeasonGamesRepository()
        self.box_score_traditional_repository = BoxScoreTraditionalRepository()

    def prepare_data_for_logistic_regression(self, team_id: str) -> pd.DataFrame:
        results = self.season_games_repository.get_games_by_team(
            team_id=team_id, limit=100)

        result_data = []
        for game in results:
            home_score = game['home_team_score']
            away_score = game['away_team_score']

            if home_score > away_score:
                if game["home_team_id"] == team_id:
                    game['winner'] = 1
                else:
                    game['winner'] = 0
            else:
                if game["away_team_id"] == team_id:
                    game['winner'] = 1
                else:
                    game['winner'] = 0

            rebounds_total = 0
            assists_total = 0

            for scores in self.box_score_traditional_repository.fetch_all_box_scores_for_game_id(
                    game_id=game['game_id']):
                rebounds_total += scores[19]
                assists_total += scores[20]

            result_data.append({
                "rebounds_total": rebounds_total,
                "assists_total": assists_total,
                "winner": game['winner']
            })

        df = pd.DataFrame(result_data)

        X = df[["rebounds_total", "assists_total"]]
        y = df["winner"]

        X = np.c_[np.ones(X.shape[0]), X]  # adds a column of 1s

        # Initialize theta
        theta = np.zeros((X.shape[1], 1))

        # Gradient descent loop
        for _ in range(LogisticRegressionAnalyzer.GRADIENT_DESCENT_ITERATIONS):
            z = X @ theta
            h = 1 / (1 + np.exp(-z))  # sigmoid
            gradient = X.T @ (h - y.values.reshape(-1, 1)) / len(y)
            theta -= LogisticRegressionAnalyzer.LEARNING_RATE * gradient

        print("Coefficients (θ):", theta)


if __name__ == "__main__":
    analyzer = LogisticRegressionAnalyzer()
    analyzer.prepare_data_for_logistic_regression(
        team_id="1610612766")  # Example team ID
