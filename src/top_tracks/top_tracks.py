from flask import Flask
from flask import render_template, request, url_for, redirect
from flask import current_app, abort
from flask import Blueprint

import re
import requests
import soundcloud

top_tracks = Blueprint('top_tracks', __name__,
        static_folder='static', static_url_path='/static/top_tracks',
        template_folder='templates')


@top_tracks.route('/top_tracks', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('tt.html', description=True)

    elif request.method == 'POST':
        artist = request.form.get('artist', '')
        artist = artist.strip()

        if artist and re.match('^[a-z0-9_-]+$', artist, re.I):
            return redirect(url_for('top_tracks.track_list', artist=artist))
        else:
            if artist:
                error = 'Invalid username: {}'.format(artist)
            else:
                error = 'Invalid username'
            return render_template('tt.html', artist=artist, error=error)


class Track:
    def __init__(self, track, client):
        self.id = track.id
        self.title = track.title
        self.plays = getattr(track, 'playback_count', 0)

        self.client = client

    def get_stream_url(self):
        stream_url = self.client.get(self.stream, allow_redirects=False)
        return stream_url.location

    def __lt__(self, other):
        return self.plays < other.plays


@top_tracks.route('/top_tracks/<artist>')
def track_list(artist=None):
    if not artist or not re.match('^[a-z0-9_-]+$', artist, re.I):
        if artist:
            error = 'Invalid username: {}'.format(artist)
        else:
            error = 'Invalid username'
        return render_template('tt.html', artist=artist, error=error)

    if 'SC_CLIENT_ID' not in current_app.config:
        abort(500)

    client = soundcloud.Client(client_id=current_app.config['SC_CLIENT_ID'])

    try:
        user_id = client.get('/resolve', url='http://soundcloud.com/' + artist).id
    except requests.exceptions.HTTPError:
        error = 'User "{}" not found'.format(artist)
        return render_template(artist=artist, error=error)

    songs = []
    next_href = '/users/{}/tracks'.format(user_id)

    while True:
        tracks = client.get(next_href, limit=200, linked_partitioning=1)
        for track in tracks.collection:
            songs.append(Track(track, client))

        if not hasattr(tracks, 'next_href'):
            break

        next_href = tracks.next_href

    songs = sorted(songs, reverse=True)

    return render_template('tt.html', artist=artist, songs=songs[:20])
