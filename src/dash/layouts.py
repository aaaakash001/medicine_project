from flask import current_app
from dash import html, dcc, dash_table
from src.main.utils import get_medicine_data


def get_medicine_data_in_context(*args, **kwargs) -> list[dict]:
    with current_app.app_context():
        return get_medicine_data(*args, **kwargs)


# Defining layout
compositionLayout = html.Div([
    dcc.Dropdown(
        id='composition-dropdown',
        options=[
            {'label': row['composition'], 'value': row['composition']}
            for row in get_medicine_data_in_context(
                columns=["composition"],
                distinct=True
            )
        ],
        value=get_medicine_data_in_context(
            columns=["composition"],
            distinct=True)[0]["composition"]
    ),

    dash_table.DataTable(
        id='table',
        columns=[
            {
                'name': col,
                'id': col
            } for col in ['brand', 'name', 'type', 'price']
        ],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])


# ////////////////////////////////////////////////////////////////////////////////////////////


# Defining layout
brandsLayout = html.Div([
    dcc.Dropdown(
        id='brand-dropdown',
        options=[
            {'label': row['brand'], 'value': row['brand']}
            for row in get_medicine_data_in_context(
                columns=["brand"], distinct=True
            )
        ],
        value=get_medicine_data_in_context(
            columns=["brand"], distinct=True
        )[0]["brand"]
    ),

    dash_table.DataTable(
        id='table',
        columns=[
            {
                'name': col,
                'id': col
            } for col in ['name', 'composition', 'type', 'price']
        ],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])
