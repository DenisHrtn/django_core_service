#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Starting Celery..."
exec poetry run celery -A django_core_service worker --loglevel=info &
           poetry run celery -A django_core_service beat --loglevel=info