from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from nba_scraper.dao.csv_dao.csv_box_score_dao import CSVBoxScoreDAO
from nba_scraper.models.game_box_score import GameBoxScore
from nba_scraper.models.box_score_row import BoxScoreRow
from nba_scraper.utils import Utils


class Analyzer:

    def rebounds_against_wins(self, team: str, season: str):
        """
            Count the number of rebounds and see how many wins
        """

        box_scores: list[GameBoxScore] = CSVBoxScoreDAO.get_by_team_and_season(
            team, season)

        game_pairs = self._get_game_pairs(box_scores)

        home_team_wins = [self._is_home_team_winner(
            box_score_pair) for box_score_pair in game_pairs]

        home_team_rebounds = [self._get_home_team(box_score_pair).get_sum_of_column(
            BoxScoreRow.Fields.TRB) for box_score_pair in game_pairs]

        away_team_rebounds = [self._get_away_team(box_score_pair).get_sum_of_column(
            BoxScoreRow.Fields.TRB) for box_score_pair in game_pairs]

        return pd.DataFrame({
            "Home Team Rebounds": home_team_rebounds,
            "Away Team Rebounds": away_team_rebounds,
            "Home Team Wins": home_team_wins
        })

    def _get_game_pairs(self, box_scores: list[GameBoxScore]) -> list[list[GameBoxScore]]:
        """
            Get the box score for both the home and away team
        """
        box_score_pairs = defaultdict(list)
        for box_score in box_scores:
            key = Utils.get_game_id_prefix(box_score.id)
            box_score_pairs[key].append(box_score)
        return [box_score_pair for box_score_pair in box_score_pairs.values()]

    def _is_home_team_winner(self, box_score_pair: list[GameBoxScore]) -> bool:
        """
            Check if the home team won
        """
        home_team_box_score = self._get_home_team(box_score_pair)
        away_team_box_score = self._get_away_team(box_score_pair)

        return home_team_box_score.get_sum_of_column(
            BoxScoreRow.Fields.PTS.value) > away_team_box_score.get_sum_of_column(BoxScoreRow.Fields.PTS.value)

    def _get_home_team(self, box_score_pair: list[GameBoxScore]) -> GameBoxScore:
        """
            Extract the home team initials from the box score ID
        """
        home_team = Utils.get_home_team(box_score_pair[0].id)
        home_team_box_score = [
            box_score for box_score in box_score_pair if Utils.get_stat_team(box_score.id) == home_team]
        return home_team_box_score[0]

    def _get_away_team(self, box_score_pair: list[GameBoxScore]) -> GameBoxScore:
        """
            Extract the away team initials from the box score ID
        """
        stat_team = Utils.get_stat_team(box_score_pair[0].id)
        home_team = Utils.get_home_team(box_score_pair[0].id)
        away_team_box_score = [
            box_score for box_score in box_score_pair if box_score.id[-7:] == home_team + "_" + stat_team]
        return away_team_box_score[0]


if __name__ == "__main__":

    analyzer = Analyzer()

    out_rebound_win_list, out_rebound_loss_list, under_rebound_win_list, under_rebound_loss_list = [], [], [], []
    for team in ["LAC", "LAL"]:
        rebound_stats = analyzer.rebounds_against_wins(team, 2023)

        rebound_stats["Rebound Diff"] = (
            rebound_stats["Home Team Rebounds"] -
            rebound_stats["Away Team Rebounds"]
        )

        # Define categories
        out_rebound = rebound_stats["Rebound Diff"] > 0
        win = rebound_stats["Home Team Wins"]

        # Compute counts
        out_rebound_win = ((out_rebound) & (win)).sum()
        out_rebound_loss = ((out_rebound) & (~win)).sum()
        under_rebound_win = ((~out_rebound) & (win)).sum()
        under_rebound_loss = ((~out_rebound) & (~win)).sum()

        out_rebound_win_list.append(out_rebound_win)
        out_rebound_loss_list.append(out_rebound_loss)
        under_rebound_win_list.append(under_rebound_win)
        under_rebound_loss_list.append(under_rebound_loss)

        # print(f"[{team}] Home team out-rebounded and won:", out_rebound_win)
        # print(f"[{team}] Home team out-rebounded but lost:", out_rebound_loss)
        # print(f"[{team}] Home team were out-rebounded and won:",
        #       under_rebound_win)
        # print(f"[{team}] Home team were out-rebounded and lost:",
        #       under_rebound_loss)
