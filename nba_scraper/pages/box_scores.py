import os
import dash_bootstrap_components as dbc
from dash import dcc, html
from nba_scraper.configuration.box_score import DIRECTORY_PATH
from nba_scraper.pages.page import Page


class BoxScorePage(Page):

    @staticmethod
    def box_score_page_layout():
        games = BoxScorePage.get_games()

        return dbc.Container([
            Page.navigation_bar(),
            html.H1("Box Scores Dashboard"),

            html.H2("Box Scores"),
            html.Label("Select Game"),
            dcc.Dropdown(
                id='box-score-dropdown',
                options=[
                    {'label': BoxScorePage._format_game_name(game),
                     'value': BoxScorePage._format_game_name(game)}
                    for game in games
                ],
                value=None,
                clearable=True
            ),
            html.Div(id='box-score-container'),
        ])

    @staticmethod
    def get_games():
        all_games = os.listdir(DIRECTORY_PATH + "total_box_scores/")

        return [game for game in all_games if int(game[:8]) > 20241001]

    @staticmethod
    def _format_game_name(game):
        game_name = ""

        game_name += game[:4] + "-"
        game_name += game[4:6] + "-"
        game_name += game[6:8] + " at "
        game_name += game[9:12] + " : "
        game_name += game[13:16]

        return game_name
