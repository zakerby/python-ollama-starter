import datetime
from flask_login import UserMixin
from ..extensions import db


class User(db.Model, UserMixin):
    """User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, 
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username