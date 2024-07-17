import os
from os import environ
import typing_extensions
import datetime
import urllib.parse

import flask_sqlalchemy
import sqlalchemy
import sqlalchemy.orm as orm


# annotated types for usage with Mapped[]
# auto-incrementing type, useful for generating IDs
serial = typing_extensions.Annotated[
    int,
    sqlalchemy.Sequence(start=0, increment=1, name='Sequence'),
    sqlalchemy.orm.mapped_column(sqlalchemy.BIGINT, primary_key=True)
]

# longest 8 byte signed integer
long_int = typing_extensions.Annotated[
    int,
    sqlalchemy.orm.mapped_column(sqlalchemy.BIGINT, nullable=False)
]

# 2 byte int
small_int = typing_extensions.Annotated[
    int,
    sqlalchemy.orm.mapped_column(sqlalchemy.SMALLINT, nullable=False)
]

# 4 byte int
mid_int = typing_extensions.Annotated[
    int,
    sqlalchemy.orm.mapped_column(sqlalchemy.INTEGER, nullable=False)
]

# fixed string types
fixed_strings = dict([
    (size, typing_extensions.Annotated[str, sqlalchemy.orm.mapped_column(sqlalchemy.CHAR(size), nullable=False)])
    for size in [16, 32, 64, 128, 256]
])

# string types
variable_strings = dict([
    (size, typing_extensions.Annotated[str, sqlalchemy.orm.mapped_column(sqlalchemy.VARCHAR(size), nullable=False)])
    for size in [16, 32, 64, 128, 256]
])

# 15 digits precision floating point number
c_double = typing_extensions.Annotated[
    float,
    sqlalchemy.orm.mapped_column(sqlalchemy.DOUBLE, nullable=False)
]

# 7 digits precision floating point number
c_float = typing_extensions.Annotated[
    float,
    sqlalchemy.orm.mapped_column(sqlalchemy.FLOAT, nullable=False)
]

# date + time date - (6.5.2004) time - 20:18, datetime - 6.5.2004 20:18:20
c_datetime = typing_extensions.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(sqlalchemy.TIMESTAMP, nullable=False, default=sqlalchemy.func.current_timestamp())
]

c_datetime_fired = typing_extensions.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(sqlalchemy.TIMESTAMP, nullable=True, default=None)
]

# date (6.5.2004)
c_date = typing_extensions.Annotated[
    datetime.date,
    sqlalchemy.orm.mapped_column(sqlalchemy.DATE, nullable=False)
]


class ModelBase(sqlalchemy.orm.DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(self._build_url(), echo=True, pool_size=5)
        self.session = orm.sessionmaker(self.engine)

    def _build_url(self):
        url = sqlalchemy.URL.create(
            'postgresql',
            username=os.getenv('POSTGRES_USER'),
            password=urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD')),
            host=os.getenv('SERVER_POSTGRES_HOSTNAME'),
            port=os.getenv('POSTGRES_CONTAINER_PORT'),
            database=os.getenv('POSTGRES_DATABASE')
        )
        return url

    def get_session(self):
        return self.session

    def create_tables(self):
        ModelBase.metadata.create_all(bind=self.engine)


db = Database()
