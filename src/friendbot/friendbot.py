from flask import Flask, Blueprint, jsonify, current_app, \
                  request, abort, url_for, redirect

import csv
import os
import random

friendbot = Blueprint('fb', __name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


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


def get_name_from_id(id):
    with open(os.path.join(APP_ROOT, 'slack_ids.csv')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['slack_id'] == id:
                return row['name']
        return None


@friendbot.route('/friendbot.py', methods=['GET', 'POST'])
@friendbot.route('/friendbot', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        abort(405)

    form = request.form
    trigger_word = form.get('trigger_word', '')
    text = form.get('text', '')
    domain = form.get('team_domain', '')
    user = form.get('user_name', '${name}')

    if domain != 'thelonelybear':
        abort(400)

    if trigger_word.startswith('!') and trigger_word.endswith('bot'):
        friend = trigger_word[1:-3]
    elif trigger_word.startswith('<@'):
        # This is a file upload, ignore it
        if ('uploaded a file:' in text or
                'commented on' in text or
                'set the' in text):
            return jsonify({})

        friend = get_name_from_id(trigger_word[2:])

        if friend is None:
            abort(400)
    else:
        abort(400)

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
