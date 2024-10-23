import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Import layouts for pages
from pages import home, about

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Tracks the URL
    # Container where page content will be displayed
    html.Div(id='page-content')
])

# Define the callback to update page content based on URL


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/about':
        return about.layout
    else:
        return home.layout  # Default is the home page


if __name__ == '__main__':
    app.run_server(debug=True)
