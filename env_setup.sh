#!/bin/sh
export POSTGRES_NAME=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=db
export POSTGRES_PORT=5432
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=password
export DJANGO_SUPERUSER_EMAIL=dummyemail@example.com
export DJANGO_SECRET_KEY="django-insecure-v9@wclex#ifim9k4)8_=+hoaf6+hx=8x7+8ibioay30adu1y+n"
python app/manage.py collectstatic
