from flask import Flask, Blueprint, jsonify, request, abort, current_app, \
        make_response
import random
import requests
from sqlalchemy.sql import func
from slackclient import SlackClient

from friendbot.models import Friend

import re

friendbot = Blueprint('fb', __name__)


def get_phrase(text, event):
    if text.startswith('!') and text.lower().endswith('bot'):
        text = text.lower()
        friend = Friend.query.filter_by(name=text[1:-3]).first()

    elif text.startswith('<@'):
        current_app.logger.error(text)
        # This is a file upload, ignore it
        if ('uploaded a file:' in text or
                'commented on' in text or
                'pinned ' in text or
                'joined #' in text or
                'set the' in text):
            return make_response('Ignoring', 200,)

        text = re.sub('>.*$', '', text)

        search = Friend.query.filter_by(slack_id=text[2:])

        if not search.count():
            return make_response('Friend not found', 200,)

        friend = search.first()
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

    emoji_icons = {
        'claire': ':chandyw:',
        'flora': ':flora1:',
        'max': ':max:',
        'lawrence': ':man_with_turban:'
    }

    if name == 'friendbot':
        pass
    elif name in emoji_icons:
        args['icon_emoji'] = emoji_icons[name]
    else:
        args['icon_url'] = 'https://maxtimkovich.com/img/friends/{}.jpg'.format(name)

        r = requests.get(args['icon_url'])

        if r.status_code != 200:
            return make_response("User icon not found", 200,)

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

            if ((text.startswith('!') and text.lower().endswith('bot')) or
                    text.startswith('<@')):
                return get_phrase(text, event)
            elif (re.search('ma+(x|cks)', text, re.I) or
                    re.search('swerve', text, re.I)):
                sc = SlackClient(current_app.config['SLACK_BOT_TOKEN'])

                sc.api_call(
                    'reactions.add',
                    channel=event['channel'],
                    timestamp=event['ts'],
                    name='max',
                )

                return make_response("Mission Complete!", 200,)

    return make_response('Not for friendbot', 200,)

characters = {
    ' ': '-----',
    '.': '00001',
    '!': '11101',
    'a': '75755',
    'b': '75757',
    'c': '71117',
    'd': '35553',
    'e': '71717',
    'f': '71711',
    'g': '71757',
    'h': '55755',
    'i': '72227',
    'j': '44457',
    'k': '55355',
    'l': '11117',
    'm': '57555',
    'n': '75555',
    'o': '75557',
    'p': '75711',
    'q': '75744',
    'r': '75355',
    's': '71747',
    't': '72222',
    'u': '55557',
    'v': '55552',
    'w': '55575',
    'x': '55255',
    'y': '55222',
    'z': '74717',
}

display = {
    '7': 'ccc',
    '5': 'c c',
    '4': '  c',
    '3': 'cc ',
    '2': ' c ',
    '1': 'c  ',
    '0': '   ',
}

def emotifier(emote, phrase):
    output = ''
    for i in range(5):
        for c in phrase:
            line = characters[c][i]

            if line == '-':
                output += ':blank:'
                continue

            line_out = display[line]

            line_out = line_out.replace(' ', ':blank:')
            line_out = line_out.replace('c', emote)

            output += line_out + '    '

        output += '\n'

    return output


@friendbot.route('/emotify', methods=['POST'])
def emotify():
    form = request.form

    if form.get('token', '') != current_app.config['SLACK_VERIFY_TOKEN']:
        return make_response('', 200,)

    text = form.get('text', '')

    if not text:
        return make_response("Request can't be empty :max:", 200,)

    text = text.lower()
    split = text.split()
    emote = split[0]
    phrase = ' '.join(split[1:])

    if emote[0] != ':' or emote[-1] != ':':
        return make_response("Emotes start and end with ':' :max:", 200,)
    elif not re.search('^[a-z.! ]+$', phrase):
        return make_response("Invalid phrase. Phrases can only be composed of letters, spaces, '.', and '!' :max:", 200,)

    return jsonify({
        'response_type': 'in_channel',
        'text': emotifier(emote, phrase),
    })

the_asians = {
    'claire': '@U40UP9YEN',
    'carl': '@U410XHHLM',
    'ben': '@U45VC1JDQ',
    'jay': '@U407FJ7KK',
    'bobo': '@U407JD1K3',
    'henry': '@U7SCBA9RN',
    'rose': '@U7C5JF4FQ',
    'will': '@U858K8M19',
    'bump': '@U920CGV29',
    'pearl': '@U91GKF55F',
    'flora': '@U45DQ47EV',
    'tony': '@U8F69PJ1Y',
    'ernest': '@U407EU12M',
    'mindy': '@U40TVQN1H',
    'kai': '@UA3166RGA',
    'justin': '@U406YM1JL',
}

musketeers = {
    'max': '@U410D66MA',
    'jonat': '@U40SH115Z',
    'cassidy': '@U45SYMD0A',
}


@friendbot.route('/people_ping', methods=['POST'])
def people_ping():
    form = request.form
    if form.get('token') != current_app.config['SLACK_VERIFY_TOKEN']:
        return make_response('', 200,)

    cmd = form.get('command')
    if cmd == '/asians':
        people = list(the_asians.values())
    elif cmd == '/three_musketeers':
        people = list(musketeers.values())
    elif cmd == '/halfies':
        people [the_asians['jay']]
    else:
        return make_response('Invalid command', 200,)
    
    random.shuffle(people)

    return jsonify({
        'response_type': 'in_channel',
        'text': ' '.join('<{}>'.format(n) for n in people)
    })
