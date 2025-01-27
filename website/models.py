# we create our database here

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))  # this is a one to many user, so the foreign key allows that to happen


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)  # Ensure this matches
    todo = db.relationship('Todo') # this allows us to access all the todos created or owned by a user