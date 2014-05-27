#!/bin/bash
set -e
./manage.py dumpdata --natural --indent=4  -v3 --traceback nagios.NagiosOpts > Ncheckops_data.json
./manage.py migrate nagios 0007 --fake
echo "Change the model NagiosOpts to abstract and press intro to continue"
read TRASH
./manage.py migrate nagios