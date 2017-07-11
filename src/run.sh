#!/usr/bin/env bash

source venv/bin/activate
export FLASK_APP=app.py
export FLASK_CONFIG=flask.cfg
export FLASK_DEBUG=1
exec python -m flask run
