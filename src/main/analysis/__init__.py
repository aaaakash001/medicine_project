from flask import Blueprint

analysis_bp = Blueprint('analysis_bp', __name__)

from src.main.analysis import views
