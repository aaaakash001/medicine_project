import pandas as pd
import plotly.express as px
from flask import Blueprint
from dash import Dash, html, dcc, dash_table, Input, Output
from backend.db import engine
from backend import app


composition_bp = Blueprint('composition', __name__)

compositionDashApp = Dash(__name__, server=app, url_base_pathname='/composition/')

# Function to fetch unique compositions from the database
def fetch_unique_compositions_from_db():
    query = "SELECT DISTINCT composition FROM medicine"
    compositions = pd.read_sql(query, con=engine)
    return compositions['composition'].tolist()

# Defining layout
compositionDashApp.layout = html.Div([
    dcc.Dropdown(
        id='composition-dropdown',
        options=[
            {'label': composition, 'value': composition}
            for composition in fetch_unique_compositions_from_db()
        ],
        value=fetch_unique_compositions_from_db()[0]
    ),
    
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in [ 'brand', 'name','type', 'price']],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])

# Define the update_histogram function
@compositionDashApp.callback(
    [Output('bar-chart', 'figure'),
     Output('table', 'data')],
    Input('composition-dropdown', 'value')
)
def update_histogram(selectedComposition):
    # Construct the SQL query with placeholders for user inputs
    query = "SELECT  brand,name, type, price FROM medicine WHERE composition = %s order by brand"
    
    # Use the SQLAlchemy engine to execute the query and pass the parameters
    df = pd.read_sql(query, con=engine, params=(selectedComposition,))
    
    # Create the bar chart
    fig = px.bar(df, x='brand', y='price', labels={'price': 'Price'})

    return fig, df.to_dict('records')
