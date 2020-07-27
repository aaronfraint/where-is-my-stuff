"""Initialize app."""
import os
import platform
from random import randrange
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sql_connection import URI_TUNNEL, URI_ON_SERVER

db = SQLAlchemy()
login_manager = LoginManager()


# General Config
DEBUG = True
SECRET_KEY = os.urandom(32)

# Database
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

if platform.system() == "Darwin":
    SQLALCHEMY_DATABASE_URI = URI_TUNNEL
else:
    SQLALCHEMY_DATABASE_URI = URI_ON_SERVER


def make_random_gradient(style: str = "random") -> str:

    def _make_random_rgba():
        v1 = randrange(255)
        v2 = randrange(255)
        v3 = randrange(255)

        return f"rgba({v1},{v2},{v3},X)"

    def _gradient(color: str) -> str:
        color1 = color.replace("X", "0.8")
        color2 = color.replace("X", "0")
        return f"{color1}, {color2}"

    # For now, just use random colors
    if style == "default":
        color1 = "rgba(255,0,0,X)"
        color2 = "rgba(0,255,0,X)"
        color3 = "rgba(0,0,255,X)"

    elif style == "random":
        color1 = _make_random_rgba()
        color2 = _make_random_rgba()
        color3 = _make_random_rgba()

    rot1 = randrange(360)
    rot2 = randrange(360)
    rot3 = randrange(360)

    text = f"""
        background: linear-gradient({rot1}deg, {_gradient(color1)} 70.71%),
                    linear-gradient({rot2}deg, {_gradient(color2)} 70.71%),
                    linear-gradient({rot3}deg, {_gradient(color3)} 70.71%);
    """

    return text


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # # Application Configuration
    # app.config.from_object('config.Config')

    # Pass configuration values
    app.config["DEBUG"] = DEBUG
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_ECHO"] = SQLALCHEMY_ECHO
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS



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

        from my_stuff.routes import containers
        app.register_blueprint(containers.container_bp)

        from my_stuff.routes import tag_filter
        app.register_blueprint(tag_filter.tag_bp)

        from my_stuff.routes import search
        app.register_blueprint(search.search_bp)


        # # Create Database Models
        # db.create_all()

        # # Compile static assets
        # if app.config['FLASK_ENV'] == 'development':
        #     compile_assets(app)

        return app