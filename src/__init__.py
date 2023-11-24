from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from src.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config_class)

    db.init_app(flaskApp)
    login_manager.init_app(flaskApp)
    login_manager.login_view = 'auth_bp.login'  # Specify the login view

    # Import your models to ensure they are recognized by SQLAlchemy
    from src.main.models import Medicine
    from src.auth.models import User

    with flaskApp.app_context():
        db.create_all()  # Create tables if they don't exist

    flaskApp.app_context().push()
    from src.main import main_bp
    from src.auth import auth_bp
    from src.dash import dash_bp, create_dash_app

    flaskApp.register_blueprint(main_bp)
    flaskApp.register_blueprint(auth_bp)
    flaskApp.register_blueprint(dash_bp)

    from src.dash.layouts import compositionLayout, brandsLayout
    compositionDashApp = create_dash_app(flaskApp, '/composition/', compositionLayout)
    brandsDashApp = create_dash_app(flaskApp, '/brands/', brandsLayout)

    from src.dash.callbacks import create_callback
    create_callback(compositionDashApp, 'composition')
    create_callback(brandsDashApp, 'brand')

    @login_manager.user_loader
    def load_user(user_id):
        # Specify how to load a user from the ID stored in the session
        return User.query.get(int(user_id))

    return flaskApp
