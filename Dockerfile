# syntax = docker/dockerfile:1.2

# temp stage
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/pypoetry \
    pip install --no-cache-dir poetry && \
    poetry self add poetry-plugin-export && \
    poetry config virtualenvs.create false && \
    poetry export -f requirements.txt --without-hashes -o requirements.txt && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# final stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# создаем непривилегированного пользователя app
RUN addgroup --system app && adduser --system --ingroup app app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry

# копируем wheels и устанавливаем их
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

COPY entrypoint.sh entrypoint-celery.sh ./
COPY pyproject.toml poetry.lock ./
COPY src /app/src

# даем юзеру права на выполнение скриптов
RUN chmod +x entrypoint.sh entrypoint-celery.sh && \
    chown -R app:app /app

WORKDIR /app/src

USER app