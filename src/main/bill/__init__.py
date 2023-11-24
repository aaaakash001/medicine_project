from flask import Blueprint

bill_bp = Blueprint('bill_bp', __name__)

from src.main.bill import views
