import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from .data_collector import get_nba_data_by_year_and_directory, get_total_results_by_team, WINNER
import nba_scraper.configuration.schedule_and_results as sar
from .configuration.global_config import NBA_TEAMS, YEARS

# df = get_nba_data_by_year_and_directory(
#     2024, sar.DIRECTORY_PATH)
# df[sar.DATE] = pd.to_datetime(df[sar.DATE], format="%a, %b %d, %Y")
# df = df.sort_values(by=sar.DATE)
#
# total_results = get_total_results_by_team(df).to_frame().reset_index()

SELECTED_YEAR = max(YEARS)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the dashboard
app.layout = dbc.Container([
    html.H1("NBA Games Dashboard"),

    # Dropdown menu for filtering by year
    html.Label("Select Home Team"),
    dcc.Dropdown(
        id='home-team-dropdown',
        options=[
            {'label': str(home_team), 'value': home_team}
            for home_team in NBA_TEAMS
        ],
        # Default to the first team in alpabetical order
        value=[],
        clearable=True
    ),

    # Table to display games
    html.Div(id='home-team-results-container'),

    html.H2("Total results for the season"),
    # Dropdown menu for filtering by year
    html.Label("Select Team"),
    dcc.Dropdown(
        id='team-result-dropdown',
        # options=[
        #     {'label': str(team), 'value': team}
        #     for team in sorted(df[sar.HOME_TEAM].unique())
        # ],
        value=[],
        multi=True
    ),

    # Table to display games
    html.Div(id='team-result-container')
])


@app.callback(
    Output('home-team-results-container', 'children'),
    [Input('home-team-dropdown', 'value')]
)
def update_home_team_results_table(team):

    df = get_nba_data_by_year_and_directory(SELECTED_YEAR, sar.DIRECTORY_PATH)

    # Filter data based on the selected year
    filtered_df = (df[df[sar.HOME_TEAM] == NBA_TEAMS[team]]
                   ).sort_values(by=sar.DATE)

    # Create a Dash DataTable
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)


@app.callback(
    Output('team-result-container', 'children'),
    [Input('team-result-dropdown', 'value')]
)
def update_team_result_table(teams: list):

    df = get_nba_data_by_year_and_directory(SELECTED_YEAR, sar.DIRECTORY_PATH)

    if not teams:
        filtered_df = total_results
    else:
        filtered_df = total_results[total_results[WINNER].isin(teams)]
    # Create a Dash DataTable
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)
