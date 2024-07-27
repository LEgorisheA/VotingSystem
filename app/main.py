from flask import Flask
from app.config import DevConf
from app.config import ProdConf
from app.database_handler import db

from app.routes.index import index


def create_app() -> Flask:

    # create app
    flask_app = Flask(__name__)

    # set config
    flask_app.config.from_object(DevConf)

    # create all tables
    db.create_tables(flask_app)

    # initialization blueprints
    flask_app.register_blueprint(index)
    return flask_app
