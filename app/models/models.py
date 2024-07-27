import sqlalchemy.orm as orm
from app.database_handler import db
import sqlalchemy as sqla


class User(db.engine.Model):
    _tablename_ = 'users'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    lastname: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)
    login: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False, unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)

    def __repr__(self):
        return f'User {self.name} {self.lastname}'


class Voting(db.engine.Model):
    _tablename_ = 'voting'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)

    def __repr__(self):
        return '<Voting {name}>'.format(name=self.name)


class Variant(db.engine.Model):
    _tablename_ = 'variants'

    id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, primary_key=True)
    voting_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(Voting.id))
    name: orm.Mapped[str] = orm.mapped_column(sqla.String, nullable=False)

    voting = orm.relationship(Voting, foreign_keys=voting_id)

    def __repr__(self):
        return f'Variant {self.name}'


class User2Variant(db.engine.Model):
    _tablename_ = 'user2variant'

    user_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(User.id), primary_key=True)
    variant_id: orm.Mapped[int] = orm.mapped_column(sqla.Integer, sqla.ForeignKey(Variant.id), primary_key=True)

    user = orm.relationship(User, foreign_keys=user_id)
    variant = orm.relationship(Variant, foreign_keys=variant_id)

    def __repr__(self):
        return f'user2variant with variant id {self.variant_id} and user id {self.user_id}'
