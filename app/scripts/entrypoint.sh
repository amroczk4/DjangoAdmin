#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
gunicorn -b :8000 app.wsgi:application