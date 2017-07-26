from flask import Flask, render_template, abort, redirect
from jinja2 import TemplateNotFound
import os

from top_tracks.top_tracks import top_tracks
from friendbot.friendbot import friendbot
from hearthsounds.hearthsounds import hearthsounds
from saved_posts.saved_posts import saved_posts


class Config:
    SC_CLIENT_ID = os.getenv('SC_CLIENT_ID')
    SECRET_KEY = os.getenv('SECRET_KEY', 'SUPER_SECRET_KEY')
    SAVED_DB = os.getenv('SAVED_DB', 'saved.db')

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(__name__+'.Config')
app.secret_key = app.config['SECRET_KEY']

# Blueprints
app.register_blueprint(top_tracks)
app.register_blueprint(hearthsounds)
app.register_blueprint(friendbot)
app.register_blueprint(saved_posts, url_prefix='/saved_posts')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def ise(e):
    return render_template('500.html'), 500


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
