from flask import Flask, render_template, abort, redirect
from jinja2 import TemplateNotFound

from top_tracks.top_tracks import top_tracks
from friendbot.friendbot import friendbot
from hearthsounds.hearthsounds import hearthsounds

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_envvar('FLASK_CONFIG')

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
