from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

from src.main import views
