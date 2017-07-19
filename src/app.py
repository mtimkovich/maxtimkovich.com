from flask import Flask, render_template, abort, redirect
from jinja2 import TemplateNotFound
import os

from top_tracks.top_tracks import top_tracks
from friendbot.friendbot import friendbot
from hearthsounds.hearthsounds import hearthsounds


class Config:
    SC_CLIENT_ID = os.getenv('SC_CLIENT_ID')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 0)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(__name__+'.Config')

# Blueprints
app.register_blueprint(top_tracks)
app.register_blueprint(hearthsounds)
app.register_blueprint(friendbot)


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
