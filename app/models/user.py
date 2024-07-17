from app.database_handler import ModelBase
from app.database_handler import serial
from app.database_handler import variable_strings

import sqlalchemy.orm as orm


class User(ModelBase):
    _tablename_ = 'users'

    id: orm.Mapped[serial]
    name: orm.Mapped[variable_strings[64]]
    lastname: orm.Mapped[variable_strings[64]]
    login: orm.Mapped[variable_strings[64]] = orm.mapped_column(unique=True)
    password: orm.Mapped[variable_strings[64]]

