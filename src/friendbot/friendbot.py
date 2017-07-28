from flask import Flask, Blueprint, jsonify, current_app, \
                  request, abort, url_for, redirect
from sqlalchemy.sql import func
from friendbot.models import db, Friend, Phrase

friendbot = Blueprint('fb', __name__)


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
        friend = Friend.query.filter_by(name=trigger_word[1:-3]).first()

    elif trigger_word.startswith('<@'):
        # This is a file upload, ignore it
        if ('uploaded a file:' in text or
                'commented on' in text or
                'set the' in text):
            return jsonify({})

        friend = Friend.query.filter_by(slack_id=trigger_word[2:]).first()

        if friend is None:
            abort(400)
    else:
        abort(400)

    output = friend.phrases.order_by(func.random()).first().line
    output = output.replace('${name}', user)
    output = output.replace('${newline}', '\n')

    return jsonify({'text': output})
