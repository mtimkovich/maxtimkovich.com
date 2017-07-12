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
app.register_blueprint(friendbot, url_prefix='/friendbot')
app.register_blueprint(hearthsounds, url_prefix='/hearthsounds')

@app.route('/')
@app.route('/<page>.html')
@app.route('/<page>')
def static_page(page='index'):
    try:
        return render_template('{}.html'.format(page))
    except TemplateNotFound:
        abort(404)
