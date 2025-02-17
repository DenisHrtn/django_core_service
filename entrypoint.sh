#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Creating migrations..."
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Starting Django..."
exec poetry run gunicorn -b 0.0.0.0:8000 django_core_service.wsgi:application --workers 3 --timeout 120 --log-level debug --reload