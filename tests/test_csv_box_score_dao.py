import unittest
import pandas as pd
from nba_scraper.configuration.box_score import TOTAL_BOX_SCORES_PATH
import nba_scraper.dao.csv_dao.csv_box_score_dao as bsd
import nba_scraper.mappers.box_score_mapper as bsm
from nba_scraper.models.game_box_score import GameBoxScore
from nba_scraper.models.box_score_row import BoxScoreRow


class TestCSVBoxScoreDAO(unittest.TestCase):

    """
        Starters,MP,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GmSc,+/-
        Kawhi Leonard,31:33,10,19,.526,1,5,.200,9,10,.900,1,5,6,5,2,1,6,5,30,20.7,+5
        Patrick Beverley,31:22,1,7,.143,0,5,.000,0,0,0,2,8,10,6,0,1,2,4,2,2.6,+13
        Landry Shamet,26:26,3,8,.375,2,4,.500,0,0,0,0,3,3,2,0,0,0,1,8,5.5,-1
        Patrick Patterson,17:29,1,3,.333,1,3,.333,1,2,.500,1,2,3,0,0,0,0,2,4,2.4,-2
        Ivica Zubac,9:38,4,4,1.000,0,0,0,0,0,0,1,0,1,0,0,0,0,2,8,6.7,-5
        Montrezl Harrell,38:22,7,11,.636,0,0,0,3,8,.375,2,5,7,4,1,1,3,3,17,13.3,+15
        Lou Williams,36:44,8,14,.571,1,4,.250,4,4,1.000,1,4,5,7,1,0,2,0,21,20.2,+13
        Maurice Harkless,29:10,4,7,.571,2,3,.667,0,0,0,2,2,4,0,4,2,0,5,10,12.1,+7
        JaMychal Green,19:16,4,8,.500,4,7,.571,0,0,0,1,5,6,0,0,0,1,3,12,8.0,+5
        Mfiondu Kabengele,Did Not Play,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        Terance Mann,Did Not Play,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        Johnathan Motley,Did Not Play,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        Jerome Robinson,Did Not Play,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    """

    def setUp(self):
        self.csv_box_score_dao = bsd.CSVBoxScoreDAO(TOTAL_BOX_SCORES_PATH)
        self.box_score_mapper = bsm.BoxScoreMapper()

    def test_get_box_score_model_by_id(self):

        # when fetching from db
        game_stats = self.csv_box_score_dao.get_by_id("/201910220LAC_LAC")

        # and when mapping to GameBoxScore
        game_box_score: GameBoxScore = self.box_score_mapper.map_df_to_box_score_game(
            game_stats)

        # Assert type is correct
        self.assertEqual(type(game_stats), pd.DataFrame)
        self.assertEqual(type(game_box_score), GameBoxScore)

        # Assert content is correct
        self.assertEqual(game_box_score.get_player_row("Kawhi Leonard"),
                         BoxScoreRow(True, "Kawhi Leonard", "31:33", 10, 19, .526, 1, 5, .200, 9, 10, .900, 1, 5, 6, 5, 2, 1, 6, 5, 30, 20.7, +5))
        self.assertEqual(game_box_score.get_player_row("Patrick Beverley"), BoxScoreRow(
            True, "Patrick Beverley", "31:22", 1, 7, .143, 0, 5, .000, 0, 0, 0, 2, 8, 10, 6, 0, 1, 2, 4, 2, 2.6, +13))
        self.assertEqual(game_box_score.get_player_row("Landry Shamet"), BoxScoreRow(
            True, "Landry Shamet", "26:26", 3, 8, .375, 2, 4, .500, 0, 0, 0, 0, 3, 3, 2, 0, 0, 0, 1, 8, 5.5, -1))
        self.assertEqual(game_box_score.get_player_row("Patrick Patterson"), BoxScoreRow(
            True, "Patrick Patterson", "17:29", 1, 3, .333, 1, 3, .333, 1, 2, .500, 1, 2, 3, 0, 0, 0, 0, 2, 4, 2.4, -2))
        self.assertEqual(game_box_score.get_player_row("Ivica Zubac"), BoxScoreRow(
            True, "Ivica Zubac", "9:38", 4, 4, 1.000, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 8, 6.7, -5))
        self.assertEqual(game_box_score.get_player_row("Montrezl Harrell"), BoxScoreRow(
            False, "Montrezl Harrell", "38:22", 7, 11, .636, 0, 0, 0, 3, 8, .375, 2, 5, 7, 4, 1, 1, 3, 3, 17, 13.3, +15))
        self.assertEqual(game_box_score.get_player_row("Lou Williams"), BoxScoreRow(
            False, "Lou Williams", "36:44", 8, 14, .571, 1, 4, .250, 4, 4, 1.000, 1, 4, 5, 7, 1, 0, 2, 0, 21, 20.2, +13))
        self.assertEqual(game_box_score.get_player_row("Maurice Harkless"), BoxScoreRow(
            False, "Maurice Harkless", "29:10", 4, 7, .571, 2, 3, .667, 0, 0, 0, 2, 2, 4, 0, 4, 2, 0, 5, 10, 12.1, +7))
        self.assertEqual(game_box_score.get_player_row("JaMychal Green"), BoxScoreRow(
            False, "JaMychal Green", "19:16", 4, 8, .500, 4, 7, .571, 0, 0, 0, 1, 5, 6, 0, 0, 0, 1, 3, 12, 8.0, +5))
        self.assertEqual(game_box_score.get_player_row("Mfiondu Kabengele"), BoxScoreRow(
            False, "Mfiondu Kabengele", "Did Not Play", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(game_box_score.get_player_row("Terance Mann"), BoxScoreRow(
            False, "Terance Mann", "Did Not Play", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(game_box_score.get_player_row("Johnathan Motley"), BoxScoreRow(
            False, "Johnathan Motley", "Did Not Play", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(game_box_score.get_player_row("Jerome Robinson"), BoxScoreRow(
            False, "Jerome Robinson", "Did Not Play", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
