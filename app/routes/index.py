import sqlalchemy
import flask_login

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

import app.models as models
from app.database_handler import db

index = Blueprint('index', __name__)


@index.route('/')
@index.route('/index')
@flask_login.login_required
def start_page():
    # change open voting for user
    voting_ids = set(db.impl().session.execute(sqlalchemy.select(models.User2Voting.voting_id).filter(
        models.User2Voting.user_id == current_user.id)
    ).scalars().all())
    all_voting = set(db.impl().session.execute(sqlalchemy.select(models.Voting.id).filter(
        models.Voting.closed_at.is_(None))).scalars().all())
    final_voting = all_voting - voting_ids

    if len(final_voting) == 0:
        voting = []
    else:
        voting = db.impl().session.execute(sqlalchemy.select(models.Voting).filter(
            models.Voting.id.in_(final_voting))).scalars().all()
    return render_template('index.html', voting=voting)
