import datetime
import csv
import io
import os
import plotly.express as px

import flask_login
import pandas as pd
import sqlalchemy

import flask
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user

from app.forms.forms import CreateVoting
import app.models as models
from app.database_handler import db

admin = Blueprint('admin', __name__)


def admin_required(func):
    if current_user.is_admin:
        return func
    else:
        return flask.Response(
            'У вас недостаточно прав для достуап к этой странице.',

        )


@admin.route('/create_voting', methods=['POST', 'GET'])
def create_voting():
    form = CreateVoting()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            voting_data = {
                'name': str(form.name.data),
                'fields': form.fields.data.split(';'),
            }
            print(voting_data['fields'])
        except Exception as error:
            return flask.Response(
                'Ошибка в обработке данных.',
                status=400
            )
        # creating voting
        voting = models.Voting(
            name=voting_data['name'],
            created_at=datetime.datetime.now()
        )
        db.impl().session.add(voting)
        db.impl().session.flush()

        # create variants for voting
        for name_field in voting_data['fields']:
            field = models.Variant()
            field.voting_id = voting.id
            try:
                name, detachment = name_field.split(',')
            except Exception as error:
                name, detachment = name_field, None
            field.name = name
            field.detachment = detachment
            db.impl().session.add(field)

        try:
            db.impl().session.commit()
        except Exception as error:
            db.impl().session.rollback()
            return flask.Response(
                'Произошла ошибка при создании голосования.',
                status=500
            )
        return redirect(url_for('admin.create_voting'))
    return render_template('create_voting.html', form=form)


@admin.route('/open_voting', methods=['GET'])
@flask_login.login_required
def open_voting():
    voting = db.impl().session.execute(sqlalchemy.select(
        models.Voting.id
    ).filter(models.Voting.closed_at == None)).all()
    return render_template('open_voting.html', voting=voting)


@admin.route('/close_voting', methods=['POST'])
@flask_login.login_required
def close_voting():
    voting_id = request.form.get('voting_id', None)
    if voting_id is None:
        return flask.Response(
            'Не удалось получить id голосования',
            500)
    # close voting
    voting = db.impl().session.execute(sqlalchemy.select(
        models.Voting
    ).filter(models.Voting.id == voting_id)).scalars().first()
    voting.closed_at = datetime.datetime.now()
    try:
        db.impl().session.commit()
    except Exception as error:
        db.impl().session.rollback()
        return flask.Response(
            'Не получилось закрыть голосование.',
            500)
    flask.flash('Голосование успешно закрыто.')
    return redirect(url_for('admin.open_voting'))


@admin.route('/view_chart', methods=['POST'])
@flask_login.login_required
def view_chart():
    # change variants
    variants = db.impl().session.execute(sqlalchemy.select(
        models.Variant).filter_by(voting_id=request.form.get('voting_id', None))).scalars().all()

    if not variants:
        return flask.Response(
            'Не получилось получить id голосования.',
            500)
    # craft dataframe from variants
    df_dict = {'name': [variant.name for variant in variants], 'count': [variant.count for variant in variants]}
    in_dataframe = pd.DataFrame.from_dict(df_dict)

    # crate chart from df
    fig = px.bar(in_dataframe, 'name', 'count')
    fig.write_html(f'{os.getcwd()}/app/templates/chart.html')
    return render_template('chart.html')


@admin.route('/all_charts', methods=['GET'])
def all_charts():
    voting = db.impl().session.execute(
        sqlalchemy.select(models.Voting)
    ).all()
    return render_template( 'all_charts.html', voting=voting)


@admin.route('/parse_user', methods=['POST', 'GET'])
def parse_user():
    if request.method == 'POST':
        path = str(request.form.get('path', None))
        input_detach = int(request.form.get('detachment', None))
        with open(os.getcwd() + '/app/' + path, 'r', encoding='utf-8-sig') as csv_file:
            users = csv.DictReader(csv_file, delimiter=',')
            for user in users:
                new_user = models.User()
                new_user.login = user['логин']
                new_user.password = user['пароль']
                new_user.name = user['имя']
                new_user.lastname = user['фамилия']
                new_user.detachment = input_detach
                new_user.is_admin = False
                db.impl().session.add(new_user)
        try:
            db.impl().session.commit()
        except Exception as error:
            db.impl().session.rollback()
            return flask.Response(
                'Error',
                500)
        return redirect(url_for('admin.parse_user'))
    return render_template('parse.html',)
