import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from .data_collector import get_nba_data_by_year_and_directory, get_total_results_by_team, TEAM, get_player_stats, get_top_player_stats, get_box_score_for_game
from .utils import Utils
import nba_scraper.configuration.schedule_and_results as sar
import nba_scraper.configuration.player_stats as ps
from .configuration.global_config import NBA_TEAMS, YEARS
from .pages.teams import TeamPage
from .pages.players import PlayerPage
from .pages.box_scores import BoxScorePage
import plotly.express as px


SEASON = max(YEARS)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout of the dashboard
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True)


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/players':
        return PlayerPage.player_layout()
    elif pathname == '/boxscores':
        return BoxScorePage.box_score_page_layout()
    else:
        return TeamPage.team_page_layout()


# TEAMS DASHBOARD


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
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=50,
    )


@app.callback(
    Output('team-result-container', 'children'),
    [Input('team-result-dropdown', 'value'),
     Input('season-store', 'data')]
)
def update_team_result_table(teams: list, season=SEASON):

    try:
        df = get_nba_data_by_year_and_directory(season, sar.DIRECTORY_PATH)
    except Exception as e:
        print("Error fetching data from season {}, exception: {}".format(season, e))
        return "\nNO DATA WAS FETCHED"

    total_results = get_total_results_by_team(df)

    if not teams:
        filtered_df = total_results
    else:
        converted_teams_list = Utils.convert_list_using_dictionary(
            teams, NBA_TEAMS)
        filtered_df = total_results[total_results[TEAM].isin(
            converted_teams_list)]

    # Create a Dash DataTable
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=50,
    )


@app.callback(
    Output("season-store", "data"),
    [Input('season-dropdown', 'value')]
)
def update_team_result_table(selected_season):
    if selected_season is None:
        return

    SEASON = selected_season
    return SEASON


@app.callback(
    [Output(component_id="div_data_graph", component_property="children"),
     Output(component_id="data_graph", component_property="figure")],
    [Input(component_id="team-result-dropdown", component_property="value")]
)
def data_graph(team_name):
    print("Team selected:", team_name)

    fig = px.scatter()

# PLAYER DASHBOARD


@app.callback(
    Output('player-stats-container', 'children'),
    [Input('player-dropdown', 'value')]
)
def update_home_team_results_table(player_name):
    if player_name is None:
        return "No player selected"
    df = get_player_stats(player_name, ps.DATA_DIRECTORY_PATH)

    # Create a Dash DataTable
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=50,
    )


@app.callback(
    Output('top-player-stats-container', 'children'),
    [Input("url", "pathname")]
)
def top_player_stats(_):
    df = get_top_player_stats("TRB", "2023-24").iloc[0:10]

    filtered_df = df[["Player", "TRB", "PTS", "Season", "Team"]]

    # Create a Dash DataTable
    return dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=50,
    )

# BOX SCORE DASHBOARD


@app.callback(
    Output('box-score-container', 'children'),
    [Input("box-score-dropdown", "value")]
)
def fetch_box_score_game(game: str):
    df = get_box_score_for_game(game)

    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        page_size=50,
    )
