from flask import Blueprint

prescription_bp = Blueprint('prescription_bp', __name__)

from src.main.prescription import views
