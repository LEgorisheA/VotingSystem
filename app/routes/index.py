import sqlalchemy
import app.models as models

from flask import Blueprint, render_template
from app.database_handler import db

index = Blueprint('index', __name__)


@index.route('/')
@index.route('/index')
def start_page():
    user = models.User(
        name='vladislav',
        lastname='Koshelnikov'
    )
    db.impl().session.add(user)
    db.impl().session.commit()
    return render_template('index.html')
