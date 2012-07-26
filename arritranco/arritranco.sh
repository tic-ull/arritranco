#!/bin/bash

cd $(dirname $0)
pwd
test -e ../virtualenv && VIRTUALENV=../virtualenv
test -e virtualenv && VIRTUALENV=virtualenv
source $VIRTUALENV/bin/activate
#export PYTHONPATH=$PYTHONPATH:$(pwd)
#$VIRTUALENV/bin/python manage.py release_sem
#DJANGO_SETTINGS_MODULE=arritranco.settings
exec $VIRTUALENV/bin/gunicorn_django $*
