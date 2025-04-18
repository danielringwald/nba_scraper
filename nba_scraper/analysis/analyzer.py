from utils import Utils
import nba_scraper.configuration.box_score as bs
from ..data_collector import get_box_scores_by_team_and_season
import matplotlib.pyplot as plt


class Analyzer:

    def rebounds_against_wins(team: str, season: str):
        # Count the number of rebounds and see how many wins

        box_scores = get_box_scores_by_team_and_season(team, season)


if __name__ == "__main__":
    pass
