from flask import Flask, render_template
from top_tracks.top_tracks import top_tracks
from friendbot.friendbot import friendbot

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_envvar('FLASK_CONFIG')

app.register_blueprint(top_tracks)
app.register_blueprint(friendbot, url_prefix='/friendbot')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/smash_maxpr.html')
@app.route('/smash_maxpr')
def smash_maxpr():
    return render_template('smash_maxpr.html')

@app.route('/python_tutorial.html')
@app.route('/python_tutorial')
def python_tutorial():
    return render_template('python_tutorial.html')

@app.route('/lisp_tutorial.html')
@app.route('/lisp_tutorial')
def lisp_tutorial():
    return render_template('lisp_tutorial.html')

@app.route('/random_caps.html')
@app.route('/random_caps')
def random_caps():
    return render_template('random_caps.html')

@app.route('/textarea.html')
@app.route('/textarea')
def textarea():
    return render_template('textarea.html')
