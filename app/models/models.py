import datetime

from flask_login import UserMixin
import sqlalchemy.orm as orm
from app.database_handler import db
import sqlalchemy as sqla


class User(db.engine.Model, UserMixin):
    _tablename_ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    lastname: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    login: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False, unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    detachment: orm.Mapped[int] = orm.mapped_column(sqla.Integer, nullable=False)
    is_admin: orm.Mapped[bool] = orm.mapped_column(sqla.Boolean, default=False)

    def __repr__(self):
        return f'User {self.name} {self.lastname}'


class Voting(db.engine.Model):
    _tablename_ = 'voting'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sqla.DateTime, nullable=False)
    closed_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sqla.DateTime, nullable=True)

    def __repr__(self):
        return f'Voting {self.name}, closed: {"Yes" if self.closed_at else  "No"}'

    def __init__(
            self,
            name,
            created_at=datetime.datetime.now(),
            closed_at=None
    ):
        self.name = name
        self.created_at = created_at
        self.closed_at = closed_at


class Variant(db.engine.Model):
    _tablename_ = 'variants'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    voting_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(Voting.id))
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    count: orm.Mapped[int] = orm.mapped_column(sqla.Integer, default=0)
    detachment: orm.Mapped[int] = orm.mapped_column(sqla.Integer, nullable=True, default=None)

    voting = orm.relationship(Voting, foreign_keys=voting_id)

    def __repr__(self):
        return f'Variant {self.name}'


class User2Voting(db.engine.Model):
    _tablename_ = 'user2variant'

    user_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(User.id), primary_key=True)
    voting_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(Voting.id), primary_key=True)
    variant_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(Variant.id))

    user = orm.relationship(User, foreign_keys=user_id)
    variant = orm.relationship(Variant, foreign_keys=variant_id)
    voting = orm.relationship(Voting, foreign_keys=voting_id)

    def __repr__(self):
        return f'user2variant with variant id {self.variant_id} and user id {self.user_id}'
