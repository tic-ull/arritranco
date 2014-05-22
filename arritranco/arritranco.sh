#!/bin/bash

cd $(dirname $0)
pwd
test -e ../virtualenv && VIRTUALENV=../virtualenv
test -e virtualenv && VIRTUALENV=virtualenv
source ${VIRTUALENV}/bin/activate
exec ${VIRTUALENV}/bin/gunicorn_django $*

#gunicorn arritranco.wsgi:application --bind 127.0.0.1:8000
