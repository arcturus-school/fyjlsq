import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .utils.rbac import init_role_permission
from .utils.user import add_super_user
from .blueprint import init_blueprint
from .error import init_error
from .extensions import db


def create_app():
    # create flask instance
    app = Flask(__name__, instance_relative_config=True)

    # load the config from config.py
    app.config.from_object("config")

    JWTManager(app)  # initialize JWT

    # cross-origin resource sharing
    CORS(app, resources=r"/*")

    init_blueprint(app)  # initialize blueprint

    init_error(app)  # initialize error handler

    db.init_app(app)  # initialize mysql

    with app.app_context():
        if os.getenv("FLASK_DEBUG"):
            db.drop_all()  # delete tables in development mode only

        db.create_all()  # create all tables

        init_role_permission()  # initialize rbac
        add_super_user()  # create super manager

    return app
