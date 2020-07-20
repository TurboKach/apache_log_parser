#!/bin/sh

cd /usr/src/app || exit

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations --noinput
python manage.py makemigrations logs --noinput
python manage.py migrate --noinput
python manage.py migrate logs --noinput
# populate DB with test data
python manage.py loadlog https://raw.githubusercontent.com/TurboKach/apache_log_parser/master/test_data/test_access.log
python manage.py initadmin
#python manage.py runserver 0.0.0.0:8000
gunicorn alp.wsgi:application --bind 0.0.0.0:8000
