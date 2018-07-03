from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
db = SQLAlchemy(app)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_value = db.Column(db.String(200), unique=True)
