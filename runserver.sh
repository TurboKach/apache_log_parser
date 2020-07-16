#!/bin/sh

cd /usr/src/app || exit

#export PYTHONPATH=/usr/src/app;$PYTHONPATH

python manage.py migrate --noinput
python manage.py initadmin
python manage.py runserver 0.0.0.0:8000