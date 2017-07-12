from flask import Flask, Blueprint, jsonify, current_app
from flask import request, abort, url_for

import json
import os
import random
import sys

friendbot = Blueprint('fb', __name__, static_folder='friends')


def is_comment(s):
    return s.startswith('//')


def randline(filename):
    """
    Prefix a line with // to comment it
    """
    output = ''

    with open(filename) as f:
        for line in f:
            if not is_comment(line):
                output = line
                break

        i = 1
        for line in f:
            if is_comment(line):
                continue

            if not random.randint(0, i):
                output = line
            i += 1

    return output.rstrip()

@friendbot.route('/friendbot.py', methods=['GET', 'POST'])
@friendbot.route('/friendbot', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        abort(405)

    form = request.form
    text = form.get('trigger_word', '')
    all_text = form.get('text', '')
    domain = form.get('team_domain', '')
    user = form.get('user_name', '${name}')

    if domain != 'thelonelybear':
        abort(400)

    # Map Slack IDs to names
    friend_map = {
        'U406YM1JL': 'justin',
        'U40UP9YEN': 'claire',
        'U407FJ7KK': 'jay',
        'U407EU12M': 'ernest',
        'U407JD1K3': 'boston',
        'U410D66MA': 'max',
        'U40SH115Z': 'jonat',
        'U5DQGRFHQ': 'lawrence',
    }

    if text.startswith('!') and text.endswith('bot'):
        friend = text[1:-3]
    elif text.startswith('<@'):
        # This is a file upload, ignore it
        if ('uploaded a file:' in all_text or
                'commented on' in all_text or
                'set the' in all_text):
            return jsonify({})

        friend = friend_map[text[2:]]
    else:
        abort(400)

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    friends_dir = os.path.join(APP_ROOT, 'friends')

    for txt in os.listdir(friends_dir):
        file_name = os.path.splitext(txt)[0]

        if friend == file_name:
            output = randline(os.path.join(friends_dir, txt))

            # var replacement
            output = output.replace('${name}', user)
            output = output.replace('${newline}', '\n')

            return jsonify({'text': output})

    abort(400)
