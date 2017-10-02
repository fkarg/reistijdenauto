#!/bin/sh
# Script to retrieve new data from the source, and update database.
# Actual import is done using Django. This scipt should be run inside
# the "web" service container (i.e. use docker exec to run this script).
set -x

cd /app
python manage.py retrievedata
