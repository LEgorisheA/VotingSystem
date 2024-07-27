import os
from os import environ
import typing_extensions
import datetime
import urllib.parse

from flask import Flask

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy


class ModelBase(sqlalchemy.orm.DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine = SQLAlchemy(
            model_class=ModelBase,
            engine_options={
                'client_encoding': 'utf8'
            }
        )

    def build_url(self):
        url = sqlalchemy.URL.create(
            'postgresql',
            username=os.getenv('POSTGRES_USER'),
            password=urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD')),
            host=os.getenv('POSTGRES_HOSTNAME'),
            port=os.getenv('POSTGRES_CONTAINER_PORT'),
            database=os.getenv('POSTGRES_DATABASE')
        )
        return url

    def create_tables(self, app: Flask):
        self.engine.init_app(app)
        try:
            with app.app_context():
                self.engine.create_all()
        except Exception as e:
            print(f'Error in create_tables: {str(e)}')

    def impl(self):
        return self.engine


db = Database()
