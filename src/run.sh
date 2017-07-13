#!/bin/sh

. venv/bin/activate
export FLASK_APP=app.py
export FLASK_CONFIG=flask.cfg
export FLASK_DEBUG=$(awk '/^DEBUG =/ {print $3}' $FLASK_CONFIG)
exec flask run
