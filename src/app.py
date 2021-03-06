from flask import Flask, render_template, abort, redirect
from jinja2 import TemplateNotFound
import os

from top_tracks.top_tracks import top_tracks
from friendbot.friendbot import friendbot
from announcementbot.announcementbot import announcementbot 
from hearthsounds.hearthsounds import hearthsounds
from saved_posts.saved_posts import saved_posts

from friendbot.models import db as friendbot_db
from saved_posts.models import db as saved_posts_db


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'SUPER_SECRET_KEY')

    SC_CLIENT_ID = os.getenv('SC_CLIENT_ID')

    SAVED_DB = os.getenv('SAVED_DB', 'saved.db')
    FRIENDS_DB = os.getenv('FRIENDS_DB', 'friends.db')

    SLACK_VERIFY_TOKEN = os.getenv('SLACK_VERIFY_TOKEN')
    SLACK_ANN_VERIFY_TOKEN = os.getenv('SLACK_ANN_VERIFY_TOKEN')
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

app = Flask(__name__)
application = app
app.url_map.strict_slashes = False
app.config.from_object(__name__+'.Config')
app.secret_key = app.config['SECRET_KEY']

# Blueprints
app.register_blueprint(top_tracks)
app.register_blueprint(hearthsounds)
app.register_blueprint(friendbot)
app.register_blueprint(announcementbot)
app.register_blueprint(saved_posts, url_prefix='/saved_posts')

# DB Stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_BINDS'] = {
    'friends': 'sqlite:///' + app.config['FRIENDS_DB'],
    'saved': 'sqlite:///' + app.config['SAVED_DB'],
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

friendbot_db.init_app(app)
saved_posts_db.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def ise(e):
    return render_template('500.html'), 500


@app.route('/ojt')
def ojt():
    return redirect('https://chrome.google.com/webstore/detail/quick-javascript-switcher/ahjfodbngfpdppljbkhcfhcfdagfgcnj')


@app.route('/auTO')
def auTO():
    return redirect('https://discordapp.com/api/oauth2/authorize?client_id=687888371556548680&permissions=75856&scope=bot')


@app.route('/')
@app.route('/<page>.html')
@app.route('/<page>')
def show(page='index'):
    if page == 'base':
        abort(404)

    try:
        return render_template('{}.html'.format(page))
    except TemplateNotFound:
        abort(404)
