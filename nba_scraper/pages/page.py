import dash_bootstrap_components as dbc
from dash import dcc


class Page:

    def __init__(self):
        return

    def navigation_bar():
        return dbc.Navbar(
            dbc.Container([
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dcc.Link("Teams", href="/", className="nav-link text-white text-nowrap")),
                        dbc.NavItem(
                            dcc.Link("Players", href="/players", className="nav-link text-white text-nowrap")),
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
