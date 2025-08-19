import dash_bootstrap_components as dbc
from dash import dcc, html
from nba_scraper.configuration.global_config import NBA_TEAMS, YEARS
from nba_scraper.pages.page import Page


class TeamPage(Page):

    @staticmethod
    def team_page_layout():
        return dbc.Container([
            Page.navigation_bar(),
            html.H1("NBA Games Dashboard"),

            html.H2("Select season"),
            # Dropdown menu for filtering by year
            html.Label("Select Season"),
            dcc.Dropdown(
                id='season-dropdown',
                options=[
                    {'label': str(season), 'value': season}
                    for season in YEARS
                ],
                # Default to the first team in alpabetical order
                value=Page.selected_season,
                clearable=False
            ),
            dcc.Store(id='season-store'),

            html.H2("Home games result in the season"),
            # Dropdown menu for filtering by year
            html.Label("Select Home Team"),
            dcc.Dropdown(
                id='home-team-dropdown',
                options=[
                    {'label': str(home_team), 'value': home_team}
                    for home_team in NBA_TEAMS
                ],
                # Default to the first team in alpabetical order
                value=None,
                clearable=True
            ),

            # Table to display games
            html.Div(id='home-team-results-container'),

            html.H2("Total results for the season (including playoffs)"),
            # Dropdown menu for filtering by year
            html.Label("Select Team"),
            dcc.Dropdown(
                id='team-result-dropdown',
                options=[
                    {'label': str(home_team), 'value': home_team}
                    for home_team in NBA_TEAMS
                ],
                value=None,
                multi=True
            ),

            # Table to display games
            html.Div(id='team-result-container'),

            html.H2("This is a data graph")
        ])
