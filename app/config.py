import datetime
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('FLASK_SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    DATABASE_URI = environ.get('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI =


class ProdConf(Config):
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)


class DevConf(Config):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
