import dash_bootstrap_components as dbc
from dash import dcc, html
from nba_scraper.configuration.global_config import YEARS
from nba_scraper.pages.page import Page
from nba_scraper.data_collector import get_active_players

ACTIVE_PLAYERS = get_active_players()


class PlayerPage(Page):

    @staticmethod
    def player_layout():
        return dbc.Container([
            Page.navigation_bar(),
            html.H1("Player Stats Dashboard"),

            html.H2(f"Player Stats"),
            html.Label("Select Player"),
            dcc.Dropdown(
                id='player-dropdown',
                options=[
                    {'label': str(player), 'value': player}
                    for player in ACTIVE_PLAYERS
                ],
                value=None,
                clearable=True
            ),
            html.Div(id='player-stats-container'),

            html.H2("Top Player Stats"),
            html.Div(id='top-player-stats-container'),
        ])
