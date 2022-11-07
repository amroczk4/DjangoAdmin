#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata foodrle/fixtures/foodrle.yml
python manage.py createsuperuser --no-input
gunicorn -b :8000 app.wsgi:application