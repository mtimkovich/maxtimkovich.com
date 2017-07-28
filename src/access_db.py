#!ipython -i
from flask import Flask

from friendbot.models import db as fb_db, Friend, Phrase
from saved_posts.models import db as sp_db, User, Post

"""
This file makes it easy to access SQLAlchemy
without running the app
"""

app = Flask(__name__)
app.app_context().push()

friends = '/home/protected/friends.db'
saved = '/home/protected/saved.db'

# DB Stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_BINDS'] = {
    'friends': 'sqlite:///' + friends,
    'saved': 'sqlite:///' + saved,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

fb_db.init_app(app)
sp_db.init_app(app)
