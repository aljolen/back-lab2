import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile("../config.py")

db: SQLAlchemy = SQLAlchemy(app)
jwt = JWTManager(app)

import webapp.users
import webapp.categories
import webapp.records

with app.app_context():
    db.create_all()

