import pandas as pd
import plotly.express as px
from flask import Blueprint, render_template, jsonify, request
from dash import Dash, html, dcc, Input, Output, dash_table
from backend.db import engine, conn
from backend import app


brands_bp = Blueprint('brands', __name__)

brandsDashApp = Dash(__name__, server=app, url_base_pathname='/brands/')


@brands_bp.route('/brands')
def brands():
    return render_template('brands.html')


@brands_bp.route('/search', methods=['POST'])
def search():
    global conn
    search_term = request.form['composition']

    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Query the database
    cur.execute(
        "SELECT name,composition ,brand, type, price FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    result = cur.fetchall()

    conn.close()
    return jsonify(result)


@brands_bp.route('/suggest', methods=['GET'])
def suggest():
    global conn
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Fetch suggestions based on user input
    cur.execute(
        "SELECT distinct composition FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    suggestions = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(suggestions)


# Function to fetch unique compositions from the database
def fetch_unique_brands_from_db():
    query = "SELECT DISTINCT brand FROM medicine"
    brand = pd.read_sql(query, con=engine)
    return brand['brand'].tolist()


# Defining layout
brandsDashApp.layout = html.Div([
    dcc.Dropdown(
        id='brand-dropdown',
        options=[
            {'label': brand, 'value': brand}
            for brand in fetch_unique_brands_from_db()
        ],
        value=fetch_unique_brands_from_db()[0]
    ),

    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col}
                 for col in ['name', 'composition', 'type', 'price']],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])


# Define the update_histogram function
@brandsDashApp.callback(
    [Output('bar-chart', 'figure'),
     Output('table', 'data')],
    Input('brand-dropdown', 'value')
)
def update_histogram_brands(selectedBrands):
    # Construct the SQL query with placeholders for user inputs
    query = "SELECT  name,composition, type, price FROM medicine WHERE brand = %s order by name"

    # Use the SQLAlchemy engine to execute the query and pass the parameters
    df = pd.read_sql(query, con=engine, params=(selectedBrands,))

    # Create the bar chart
    fig = px.scatter(df, x='composition', y='price', labels={'price': 'Price'})

    return fig, df.to_dict('records')
