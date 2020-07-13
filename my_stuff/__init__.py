"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()



def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():

        # Register Blueprints
        from . import auth
        app.register_blueprint(auth.auth_bp)

        from my_stuff.routes import routes
        app.register_blueprint(routes.main_bp)

        from my_stuff.routes import spaces
        app.register_blueprint(spaces.spaces_bp)

        # Create Database Models
        db.create_all()

        # # Compile static assets
        # if app.config['FLASK_ENV'] == 'development':
        #     compile_assets(app)

        return app