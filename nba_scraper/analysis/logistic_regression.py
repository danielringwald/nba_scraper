import pandas as pd
import numpy as np
from nba_scraper.dao.repository.season_games_repository import SeasonGamesRepository
from nba_scraper.dao.repository.box_score_traditional_repository import BoxScoreTraditionalRepository


REGRESSION_FEATURES = [
    "field_goals_made",
    "field_goals_attempted",
    "field_goals_percentage",
    "three_pointers_made",
    "three_pointers_attempted",
    "three_pointers_percentage",
    "free_throws_made",
    "free_throws_attempted",
    "free_throws_percentage",
    "offensive_rebounds",
    "defensive_rebounds",
    "total_rebounds",
    "assists",
    "steals",
    "blocks",
    "turnovers",
    "personal_fouls",
    "points",
    "plus_minus_points"
]


class LogisticRegressionAnalyzer:

    GRADIENT_DESCENT_ITERATIONS = 10000
    LEARNING_RATE = 0.001

    def __init__(self):
        self.season_games_repository = SeasonGamesRepository()
        self.box_score_traditional_repository = BoxScoreTraditionalRepository()

    def prepare_data_for_logistic_regression(self, team_id: str) -> pd.DataFrame:
        results = self.season_games_repository.get_games_by_team(
            team_id=team_id, limit=200)

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

            field_goals_made = 0
            field_goals_attempted = 0
            field_goals_percentage = 0
            three_pointers_made = 0
            three_pointers_attempted = 0
            three_pointers_percentage = 0
            free_throws_made = 0
            free_throws_attempted = 0
            free_throws_percentage = 0
            offensive_rebounds = 0
            defensive_rebounds = 0
            total_rebounds = 0
            assists = 0
            steals = 0
            blocks = 0
            turnovers = 0
            personal_fouls = 0
            points = 0
            plus_minus_points = 0

            for scores in self.box_score_traditional_repository.fetch_all_box_scores_for_game_id(
                    game_id=game['game_id']):
                if scores["team_id"] != team_id:
                    continue  # Only consider the specified team's stats

                field_goals_made += scores["field_goals_made"]
                field_goals_attempted += scores["field_goals_attempted"]
                field_goals_percentage += scores["field_goals_percentage"]
                three_pointers_made += scores["three_pointers_made"]
                three_pointers_attempted += scores["three_pointers_attempted"]
                three_pointers_percentage += scores["three_pointers_percentage"]
                free_throws_made += scores["free_throws_made"]
                free_throws_attempted += scores["free_throws_attempted"]
                free_throws_percentage += scores["free_throws_percentage"]
                offensive_rebounds += scores["offensive_rebounds"]
                defensive_rebounds += scores["defensive_rebounds"]
                total_rebounds += scores["total_rebounds"]
                assists += scores["assists"]
                steals += scores["steals"]
                blocks += scores["blocks"]
                turnovers += scores["turnovers"]
                personal_fouls += scores["personal_fouls"]
                points += scores["points"]
                plus_minus_points += scores["plus_minus_points"]

            result_data.append({
                "field_goals_made": field_goals_made,
                "field_goals_attempted": field_goals_attempted,
                "field_goals_percentage": field_goals_percentage,
                "three_pointers_made": three_pointers_made,
                "three_pointers_attempted": three_pointers_attempted,
                "three_pointers_percentage": three_pointers_percentage,
                "free_throws_made": free_throws_made,
                "free_throws_attempted": free_throws_attempted,
                "free_throws_percentage": free_throws_percentage,
                "offensive_rebounds": offensive_rebounds,
                "defensive_rebounds": defensive_rebounds,
                "total_rebounds": total_rebounds,
                "assists": assists,
                "steals": steals,
                "blocks": blocks,
                "turnovers": turnovers,
                "personal_fouls": personal_fouls,
                "points": points,
                "plus_minus_points": plus_minus_points,
                "winner": game['winner']
            })

        df = pd.DataFrame(result_data)

        X = df[REGRESSION_FEATURES]
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

        print("Coefficients (θ):")
        width = max(len(feature) for feature in REGRESSION_FEATURES)
        for i, feature in enumerate(REGRESSION_FEATURES):
            val = theta[i][0]
            if val > 0:
                print(f"{feature:<{width}} +{val:.4f}")
            else:
                print(f"{feature:<{width}} {val:.4f}")


if __name__ == "__main__":
    analyzer = LogisticRegressionAnalyzer()
    analyzer.prepare_data_for_logistic_regression(
        team_id="1610612766")  # Example team ID
