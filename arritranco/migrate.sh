#!/bin/bash
./manage.py migrate network
./manage.py migrate hardware 0001 --fake
./manage.py migrate hardware
./manage.py migrate inventory 0001 --fake
./manage.py migrate inventory
./manage.py migrate scheduler 0001 --fake
./manage.py migrate scheduler
./manage.py migrate sondas
./manage.py migrate nagios 0002
./manage.py loaddata monitoring/nagios/fixtures/migration_data.json
./manage.py migrate nagios
