from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(200), unique=True)
