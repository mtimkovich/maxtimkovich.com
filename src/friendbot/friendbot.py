from flask import Flask, Blueprint, jsonify, request, abort, current_app, \
        make_response
from sqlalchemy.sql import func
from friendbot.models import Friend
from slackclient import SlackClient
import re

friendbot = Blueprint('fb', __name__)


def get_phrase(text, event):
    if text.startswith('!') and text.endswith('bot'):
        friend = Friend.query.filter_by(name=text[1:-3]).first()

    elif text.startswith('<@'):
        # This is a file upload, ignore it
        if ('uploaded a file:' in text or
                'commented on' in text or
                'set the' in text):
            return make_response('Ignoring', 200,)

        text = re.sub('>.*$', '', text)

        friend = Friend.query.filter_by(slack_id=text[2:]).first()

        if friend is None:
            return make_response('Friend not found', 200,)
    else:
        return make_response('Not a friendbot request', 200,)

    output = friend.phrases.order_by(func.random()).first().line
    output = output.replace('${newline}', '\n')

    sc = SlackClient(current_app.config['SLACK_BOT_TOKEN'])

    name = friend.name

    args = {
        'username': name + 'bot',
        'channel': event['channel'],
        'text': output,
        'parse': 'full'
    }

    if name != 'friendbot':
        args['icon_url'] = 'https://maxtimkovich.com/img/friends/{}.jpg'.format(name)

    sc.api_call(
        'chat.postMessage',
        **args
    )

    return make_response('Mission accomplished', 200,)


@friendbot.route('/friendbot', methods=['POST'])
def index():
    TOKEN = current_app.config['SLACK_VERIFY_TOKEN']
    form = request.get_json()

    # current_app.logger.error(form)

    if form['token'] != TOKEN:
        abort(403)

    type = form['type']

    if type == 'url_verification':
        return jsonify({'challenge': form['challenge']})

    elif type == 'event_callback':
        event = form['event']
        event_type = event['type']

        if event.get('subtype', '') == 'bot_message':
            return make_response("Please don't respond to other bots", 200,)

        if event_type == 'message':
            text = event.get('text', '')

            if ((text.startswith('!') and text.endswith('bot')) or
                    text.startswith('<@')):
                return get_phrase(text, event)
            elif re.search('ma+x', text, re.I):
                sc = SlackClient(current_app.config['SLACK_BOT_TOKEN'])

                sc.api_call(
                    'reactions.add',
                    channel=event['channel'],
                    timestamp=event['ts'],
                    name='max',
                )

                return make_response("Mission Complete!", 200,)

    return make_response('Not for friendbot', 200,)
