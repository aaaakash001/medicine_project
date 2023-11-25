from flask import Flask

app = Flask(__name__, static_folder="static")

from backend.routes.main_routes import *
from backend.routes.composition_routes import composition_bp
from backend.routes.brands_routes import brands_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.prescription_routes import prescription_bp
from backend.routes.analysis_routes import analysis_bp
from backend.routes.bill_routes import bill_bp

app.register_blueprint(admin_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(bill_bp)
app.register_blueprint(brands_bp)
app.register_blueprint(composition_bp)
app.register_blueprint(prescription_bp)

if __name__ == '__main__':
    app.run(debug=True)
