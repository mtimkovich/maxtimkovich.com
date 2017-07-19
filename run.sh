#!/bin/sh

. venv/bin/activate
export FLASK_APP=src/app.py

# Get config stuff
. ../flask_conf.sh
exec flask run
