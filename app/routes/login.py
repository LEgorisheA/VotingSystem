import flask
from flask import Blueprint, session, redirect, url_for, request, render_template
import sqlalchemy as sqla
from flask_login import login_user

from app.forms.forms import Login
import app.models as models
from app.database_handler import db

login = Blueprint('login', __name__)


@login.route('/authorization', methods=['POST', 'GET'])
def authorization():
    form = Login()
    if request.method == 'POST' and form.validate_on_submit():
        user = db.impl().session.query(models.User).filter_by(
            login=form.login.data,
            password=form.password.data
        ).first()
        if user:
            login_user(user)
            return redirect(url_for('index.start_page'))
        flask.flash('Неверный логин или пароль.', category='error')
        return redirect(url_for('login.authorization'))
    return render_template('login.html', form=form)


@login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.authorization'))
