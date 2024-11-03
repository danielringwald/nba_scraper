import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from .data_collector import get_nba_data_by_year_and_directory, get_total_results_by_team, TEAM
from .utils import Utils
import nba_scraper.configuration.schedule_and_results as sar
from .configuration.global_config import NBA_TEAMS, YEARS


SEASON = max(YEARS)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the dashboard
app.layout = dbc.Container([
    html.H1("NBA Games Dashboard"),

    html.H2(f"Select season"),
    # Dropdown menu for filtering by year
    html.Label("Select Season"),
    dcc.Dropdown(
        id='season-dropdown',
        options=[
            {'label': str(season), 'value': season}
            for season in YEARS
        ],
        # Default to the first team in alpabetical order
        value=SEASON,
        clearable=False
    ),
    dcc.Store(id='season-store'),

    html.H2(f"Home games result in the season {SEASON}"),
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

    html.H2("Total results for the season"),
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
    html.Div(id='team-result-container')
])


@app.callback(
    Output('home-team-results-container', 'children'),
    [Input('home-team-dropdown', 'value'),
     Input('season-store', 'data')]
)
def update_home_team_results_table(team, season=SEASON):
    if team is None:
        return "No team selected"

    df = get_nba_data_by_year_and_directory(season, sar.DIRECTORY_PATH)

    # Filter data based on the selected year
    filtered_df = (df[df[sar.HOME_TEAM] == NBA_TEAMS[team]]
                   ).sort_values(by=sar.DATE)

    # Create a Dash DataTable
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)


@app.callback(
    Output('team-result-container', 'children'),
    [Input('team-result-dropdown', 'value'),
     Input('season-store', 'data')]
)
def update_team_result_table(teams: list, season=SEASON):

    df = get_nba_data_by_year_and_directory(season, sar.DIRECTORY_PATH)
    total_results = get_total_results_by_team(df)

    if not teams:
        filtered_df = total_results
    else:
        converted_teams_list = Utils.convert_list_using_dictionary(
            teams, NBA_TEAMS)
        filtered_df = total_results[total_results[TEAM].isin(
            converted_teams_list)]

    # Create a Dash DataTable
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)


@app.callback(
    Output("season-store", "data"),
    [Input('season-dropdown', 'value')]
)
def update_team_result_table(selected_season):
    if selected_season is None:
        return

    SEASON = selected_season
    return SEASON
