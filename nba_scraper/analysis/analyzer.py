from collections import defaultdict
from typing import Union
import pandas as pd
from nba_scraper.dao.csv_dao.csv_box_score_dao import CSVBoxScoreDAO
from nba_scraper.models.game_box_score import GameBoxScore
from nba_scraper.models.box_score_row import BoxScoreRow
from nba_scraper.utils import Utils


class Analyzer:

    def columns_against_wins(self,
                             team: str,
                             season: Union[int, list[int], str],
                             column_enum: Union[BoxScoreRow.Fields, list[BoxScoreRow.Fields], str]) -> pd.DataFrame:
        """
            Count the number of rebounds and see how many wins
        """

        box_scores: list[GameBoxScore] = CSVBoxScoreDAO.get_by_team_and_season(
            team, season)

        game_pairs = self._get_game_pairs(box_scores)

        home_team_wins = [self._is_home_team_winner(
            box_score_pair) for box_score_pair in game_pairs]

        home_team_column, stat_team_column = self._sum_of_columns(
            game_pairs, column_enum)

        home_team_game_id = [home_team[0] for home_team in home_team_column]
        stat_team_game_id = [stat_team[0] for stat_team in stat_team_column]
        home_team_column = [home_team[1] for home_team in home_team_column]
        stat_team_column = [stat_team[1] for stat_team in stat_team_column]

        return pd.DataFrame({
            "Home Team Game ID": home_team_game_id,
            f"Home Team {column_enum}": home_team_column,
            "Stat Team Game ID": stat_team_game_id,
            f"Stat Team {column_enum}": stat_team_column,
            f"{column_enum} Diff": [home - stat for home, stat in zip(home_team_column, stat_team_column)],
            "Home Team Wins": home_team_wins
        })

    def _sum_of_columns(self,
                        game_pairs: list[list[GameBoxScore]],
                        column_enum: Union[BoxScoreRow.Fields, list[BoxScoreRow.Fields]]) -> tuple[list[int], list[int]]:

        home_team_column = [(Utils.get_game_id_prefix(box_score_pair[0].id), self._get_home_team(box_score_pair).get_sum_of_column(
            column_enum)) for box_score_pair in game_pairs]
        stat_team_column = [(Utils.get_game_id_prefix(box_score_pair[0].id), self._get_stat_team(box_score_pair).get_sum_of_column(
            column_enum)) for box_score_pair in game_pairs]

        return home_team_column, stat_team_column

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
        stat_team_box_score = self._get_stat_team(box_score_pair)

        return home_team_box_score.get_sum_of_column(
            BoxScoreRow.Fields.PTS.value) > stat_team_box_score.get_sum_of_column(BoxScoreRow.Fields.PTS.value)

    def _get_home_team(self, box_score_pair: list[GameBoxScore]) -> GameBoxScore:
        """
            Extract the home team initials from the box score IDs
        """
        home_team = Utils.get_home_team(box_score_pair[0].id)
        home_team_box_score = [
            box_score
            for box_score in box_score_pair
            if Utils.get_stat_team(box_score.id) == home_team
        ]

        return home_team_box_score[0]

    def _get_stat_team(self, box_score_pair: list[GameBoxScore]) -> GameBoxScore:
        """
            Extract the away team initials from the box score IDs
        """
        home_team = Utils.get_home_team(box_score_pair[0].id)
        stat_team_1 = Utils.get_stat_team(box_score_pair[0].id)
        stat_team_2 = Utils.get_stat_team(box_score_pair[1].id)

        stat_team = stat_team_1 if stat_team_1 != home_team else stat_team_2

        stat_team_box_score = [
            box_score
            for box_score in box_score_pair
            if box_score.id[-7:] == home_team + "_" + stat_team and home_team != stat_team
        ]

        return stat_team_box_score[0]


if __name__ == "__main__":

    analyzer = Analyzer()

    out_rebound_win_percentage_list = []
    out_rebound_loss_percentage_list = []
    under_rebound_win_percentage_list = []
    under_rebound_loss_percentage_list = []
    for team_name in ["LAC"]:
        stat_column = BoxScoreRow.Fields.PTS.value

        rebound_stats = analyzer.columns_against_wins(
            team_name, 2023, stat_column)

        if (len(rebound_stats) == 0):
            print(f"No data available for {team_name} in 2023 season.")
            raise ValueError(
                f"No data available for {team_name} in 2023 season.")

        rebound_stats["Rebound Diff"] = (
            rebound_stats[f"Home Team {stat_column}"] -
            rebound_stats[f"Stat Team {stat_column}"]
        )

        # Define categories
        out_rebound = rebound_stats["Rebound Diff"] >= 0
        win = rebound_stats["Home Team Wins"]

        # Compute counts
        out_rebound_win = ((out_rebound) & (win)).sum()
        out_rebound_loss = ((out_rebound) & (~win)).sum()
        under_rebound_win = ((~out_rebound) & (win)).sum()
        under_rebound_loss = ((~out_rebound) & (~win)).sum()
        total_games = len(rebound_stats)

        out_rebound_win_percentage_list.append(out_rebound_win / total_games)
        out_rebound_loss_percentage_list.append(out_rebound_loss / total_games)
        under_rebound_win_percentage_list.append(
            under_rebound_win / total_games)
        under_rebound_loss_percentage_list.append(
            under_rebound_loss / total_games)

        print(f"[{team_name}] Home team out-rebounded and won: {out_rebound_win} ({out_rebound_win / total_games:.2%})")
        print(f"[{team_name}] Home team out-rebounded but lost: {out_rebound_loss} ({out_rebound_loss / total_games:.2%})")
        print(f"[{team_name}] Home team were out-rebounded and won: {under_rebound_win} ({under_rebound_win / total_games:.2%})")
        print(f"[{team_name}] Home team were out-rebounded and lost: {under_rebound_loss} ({under_rebound_loss / total_games:.2%})")

    print()
    print("Out-rebound win percentage:", sum(out_rebound_win_percentage_list) /
          len(out_rebound_win_percentage_list))
    print("Out-rebound loss percentage:", sum(out_rebound_loss_percentage_list) /
          len(out_rebound_loss_percentage_list))
    print("Under-rebound win percentage:", sum(under_rebound_win_percentage_list) /
          len(under_rebound_win_percentage_list))
    print("Under-rebound loss percentage:", sum(under_rebound_loss_percentage_list) /
          len(under_rebound_loss_percentage_list))
