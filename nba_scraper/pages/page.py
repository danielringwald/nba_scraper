import dash_bootstrap_components as dbc
from dash import dcc
from nba_scraper.configuration.global_config import YEARS


class Page:

    selected_season = max(YEARS)

    def __init__(self):
        return

    @staticmethod
    def navigation_bar():
        return dbc.Navbar(
            dbc.Container([
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dcc.Link("Teams", href="/teams", className="nav-link text-white text-nowrap")),
                        dbc.NavItem(
                            dcc.Link("Players", href="/players", className="nav-link text-white text-nowrap")),
                        dbc.NavItem(
                            dcc.Link("Box Scores", href="/boxscores", className="nav-link text-white text-nowrap")),
                        dbc.NavItem(
                            dcc.Link("Stats", href="/stats", className="nav-link text-white text-nowrap")),
                    ],
                    # Center the nav items
                    justified=True,
                    className="mx-auto"  # Center within container
                )
            ]),
            color="primary",
            dark=True,
            className="mb-4"
        )
