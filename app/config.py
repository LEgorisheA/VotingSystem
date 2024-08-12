import datetime
import os
from os import environ, path
from dotenv import load_dotenv

from app.database_handler import db


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = 'super_secret_key'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}".format(
        username=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('SERVER_POSTGRES_PORT'),
        host=os.getenv('SERVER_POSTGRES_HOSTNAME'),
        dbname=os.getenv('POSTGRES_DATABASE')
    )
    ECHO = True


class ProdConf(Config):
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=20)


class DevConf(Config):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=20)
