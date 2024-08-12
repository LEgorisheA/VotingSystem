# installed
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import sqlalchemy as sqla

# our modules
from app.config import DevConf
from app.config import ProdConf
from app.database_handler import db
import app.models as models

from app.routes.login import login
from app.routes.index import index
from app.routes.admin import admin
from app.routes.user import user


login_manager = LoginManager()
login_manager.login_view = 'login.authorization'


@login_manager.user_loader
def load_user(user_id):
    return db.impl().session.query(models.User).get(user_id)


def create_app() -> Flask:

    # create app
    flask_app = Flask(__name__)
    flask_app.config.from_object(DevConf)

    # initialization some modules
    Bootstrap(flask_app)
    login_manager.init_app(flask_app)
    csrf = CSRFProtect(flask_app)

    # create all tables
    db.create_tables(flask_app)

    # initialization blueprints
    flask_app.register_blueprint(index)
    flask_app.register_blueprint(login)
    flask_app.register_blueprint(admin)
    flask_app.register_blueprint(user)

    return flask_app
