import dash_bootstrap_components as dbc
from dash import dcc, html
from ..configuration.box_score import DIRECTORY_PATH
from .page import Page
import os


class BoxScorePage(Page):

    def box_score_page_layout():
        games = BoxScorePage.get_games()

        return dbc.Container([
            Page.navigation_bar(),
            html.H1("Box Scores Dashboard"),

            html.H2(f"Box Scores"),
            html.Label("Select Game"),
            dcc.Dropdown(
                id='box-score-dropdown',
                options=[
                    {'label': str(game), 'value': game}
                    for game in games
                ],
                value=None,
                clearable=True
            ),
            html.Div(id='box-score-container'),
        ])

    def get_games():
        all_games = os.listdir(DIRECTORY_PATH + "total_box_scores/")

        return [game for game in all_games if int(game[:8]) > 20241001]
