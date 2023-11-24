from flask import Blueprint

brands_bp = Blueprint('brands_bp', __name__)

from src.main.brands import views
