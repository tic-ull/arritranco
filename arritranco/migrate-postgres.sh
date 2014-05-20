#!/bin/bash
set -e
echo "Dumping data ..."
./manage.py dumpdata --natural --indent=4  -v3 --traceback --exclude admin --exclude south --exclude sites --exclude contenttypes --exclude auth --exclude sessions > ./data.json
echo "Change the Data Base in settings, CREATE the new Data Base and then press intro to continue"
read TRASH
./manage.py syncdb -v3 --all --noinput
echo "Loading data ..."
./manage.py loaddata ./data.json --traceback -v3

