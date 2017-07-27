from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    slack_id = db.Column(db.String(10), unique=True)
    phrases = db.relationship('Phrase', cascade='all,delete-orphan',
                              backref='friend', lazy='dynamic')

    def __init__(self, name, slack_id):
        self.name = name
        self.slack_id = slack_id

    def __repr__(self):
        return 'Friend(name={})'.format(self.name)


class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.Text())
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'))

    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return 'Phrase(line={})'.format(self.line)
