import flask
import flask_login

from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user
import sqlalchemy as sqla

from app.database_handler import db
import app.models as models

user = Blueprint('user', __name__)


@user.route('/voting_view')
@flask_login.login_required
def voting_view():

    voting = db.impl().session.query(models.Voting).get(request.args.get('voting_id', None))
    if voting is None:
        fields = []
    else:
        fields = db.impl().session.execute(
            sqla.select(models.Variant).filter(models.Variant.voting_id == voting.id)
        ).scalars().all()
    return render_template('voting_view.html', voting=voting, fields=fields)


@user.route('/voting_handler', methods=['POST'])
@flask_login.login_required
def voting_handler():
    # confirm voting
    info = {
        'voting_id': request.form.get('voting_id', None),
        'field_id': request.form.get('voting_field', None),
    }
    try:
        list(map(lambda keys: int(info[keys]), info))
    except Exception as error:
        return flask.Response(
            'Ошибка получения данных',
            500
        )

    # plus vote to variant
    variant = db.impl().session.execute(sqla.select(
        models.Variant
    ).filter_by(id=info['field_id'])).scalars().first()
    if variant.detachment == current_user.detachment:
        flask.flash('Вы не можете голосовать за свой отряд.')
        db.impl().session.rollback()
        return redirect(url_for('index.start_page'))
    variant.count += 1

    # create user_to_voting
    user2voting = models.User2Voting()
    user2voting.user_id = current_user.id
    user2voting.voting_id = info["voting_id"]
    user2voting.variant_id = info['field_id']
    db.impl().session.add(user2voting)
    try:
        db.impl().session.commit()
    except Exception as error:
        db.impl().session.rollback()
        return flask.Response(
            'Не получилось зарегистрировать ваш голос.',
            500
        )
    flask.flash('Вы успешно проголосовали.')
    return redirect(url_for('index.start_page'))


