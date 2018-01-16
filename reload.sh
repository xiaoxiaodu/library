#!/bin/bash
PYTHON_DIR=/usr/local/python

# $PYTHON_DIR/bin/python manage.py syncdb --noinput
python manage.py syncdb --noinput
uwsgi --reload library.pid
