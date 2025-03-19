#!/bin/bash

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Starting Celery..."

export BROKER_URL=redis://redis_fastapi:6379/0

exec poetry run celery -A django_core_service worker --loglevel=info &
poetry run celery -A django_core_service beat --loglevel=info