from flask import Blueprint
from dash import Dash


def create_dash_app(server_instance, url_base_pathname, layout):
    dash_app = Dash(
        __name__,
        server=server_instance,
        url_base_pathname=url_base_pathname
    )
    dash_app.layout = layout
    return dash_app


dash_bp = Blueprint('dash_bp', __name__, url_prefix='/dash')
