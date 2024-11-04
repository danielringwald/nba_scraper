import dash_bootstrap_components as dbc
from dash import dcc, html
from ..configuration.global_config import YEARS
from .page import Page
from ..data_collector import get_active_players

SEASON = max(YEARS)
ACTIVE_PLAYERS = get_active_players()


class PlayerPage(Page):

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
        ])
