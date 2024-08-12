from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
import wtforms as wtf


class Login(FlaskForm):
    login = wtf.StringField('Логин', validators=[InputRequired()])
    password = wtf.StringField('Пароль', validators=[InputRequired()])
    submit = wtf.SubmitField('Войти')


class CreateVoting(FlaskForm):
    name = wtf.StringField('Название для голосования', validators=[InputRequired()])
    fields = wtf.StringField('Варианты (через точку с запятой) + отряд (через запятую)', validators=[InputRequired()])
    submit = wtf.SubmitField('Создать голосование')