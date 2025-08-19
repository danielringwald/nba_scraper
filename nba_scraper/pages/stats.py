import dash_bootstrap_components as dbc
from dash import dcc, html
import logging
from nba_scraper.configuration.global_config import NBA_TEAMS, YEARS
from nba_scraper.pages.page import Page
from nba_scraper.analysis.analyzer import Analyzer
from nba_scraper.models.box_score_row import BoxScoreRow


class StatsPage(Page):

    analyzer = Analyzer()

    @staticmethod
    def stats_page_layout():
        return dbc.Container([
            Page.navigation_bar(),
            html.H1("NBA Stats Dashboard"),

            html.H2("Select season"),
            # Dropdown menu for filtering by year
            html.Label("Select Season"),
            dcc.Dropdown(
                id='season-dropdown',
                options=[
                    {'label': str(season), 'value': season}
                    for season in YEARS
                ],
                # Default to the current season set in Page
                value=Page.selected_season,
                clearable=False
            ),
            dcc.Store(id='season-store'),

            html.H2("Select team"),
            # Dropdown menu for filtering by year
            html.Label("Select Team"),
            dcc.Dropdown(
                id='team-dropdown',
                options=[
                    {'label': str(team), 'value': team}
                    for team in NBA_TEAMS
                ],
                clearable=True
            ),

            html.H2("Select stat"),
            # Dropdown menu for filtering by year
            html.Label("Select Stat"),
            dcc.Dropdown(
                id='stat-dropdown',
                options=[
                    {'label': str(stat.value), 'value': stat.value}
                    for stat in BoxScoreRow.Fields
                ],
                clearable=True
            ),

            html.Div(id='stat-container')
        ])

    @staticmethod
    def get_analyzer_data(team, season, stat):
        """
            Get the data for the selected team, season, and stat.
            This method is used in the Dash callback to update the stats table.
        """
        logging.info(
            "Fetching data for team: %s, season: %s, stat: %s", team, season, stat)
        return StatsPage.analyzer.columns_against_wins(team, season, stat)
