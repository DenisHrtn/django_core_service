# syntax = docker/dockerfile:1.2

# temp stage
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# используется кеш для poetry
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# final stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# создаем непревелигированного юезра app
RUN addgroup --system app && adduser --system --ingroup app app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY entrypoint.sh entrypoint-celery.sh ./
COPY pyproject.toml poetry.lock .env ./
COPY src /app/src

# даем юзеру права на выполнение скриптов
RUN chmod +x entrypoint.sh entrypoint-celery.sh && \
    chown -R app:app /app

WORKDIR /app/src

USER app