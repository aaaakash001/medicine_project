from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from src.main.utils import get_medicine_data


def create_callback(dash_app, column_name):
    @dash_app.callback(
        [Output('bar-chart', 'figure'),
         Output('table', 'data')],
        Input(f'{column_name}-dropdown', 'value')
    )
    def update_histogram(selectedComposition):
        data = get_medicine_data(
            search_term=selectedComposition,
            columns=[column_name, 'name', 'type', 'price'],
            similar=False,
            order_by=[(column_name, False)]
        )
        df = pd.DataFrame(data)
        graphType = px.bar if column_name == 'composition' else px.scatter
        fig = graphType(df, x=column_name, y='price', labels={'price': 'Price'})
        return fig, df.to_dict('records')

# # Define the update_histogram function
# @composition.callback(
#     [Output('bar-chart', 'figure'),
#      Output('table', 'data')],
#     Input('composition-dropdown', 'value')
# )
# def update_histogram(selectedComposition):

#     data = get_medicine_data(
#         search_term=selectedComposition,
#         columns=['brand', 'name', 'type', 'price'],
#         similar=False,
#         order_by=[('brand', False)]
#     )

#     # Convert the data to a Pandas DataFrame
#     df = pd.DataFrame(data)

#     # Create the bar chart
#     fig = px.bar(df, x='brand', y='price', labels={'price': 'Price'})

#     return fig, df.to_dict('records')


# # Define the update_histogram function
# @brands.callback(
#     [Output('bar-chart', 'figure'),
#      Output('table', 'data')],
#     Input('brand-dropdown', 'value')
# )
# def update_histogram_brands(selectedBrands):
#     # Construct the SQL query with placeholders for user inputs
#     data = get_medicine_data(
#         search_term=selectedBrands,
#         columns=['composition', 'name', 'type', 'price'],
#         similar=False,
#         order_by=[('brand', False)]
#     )

#     # Use the SQLAlchemy engine to execute the query and pass the parameters
#     df = pd.DataFrame(data)

#     # Create the bar chart
#     fig = px.scatter(df, x='composition', y='price', labels={'price': 'Price'})

#     return fig, df.to_dict('records')
