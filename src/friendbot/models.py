from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Friend(db.Model):
    __bind_key__ = 'friends'

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
    __bind_key__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.Text())
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'))

    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return 'Phrase(line={})'.format(self.line)
