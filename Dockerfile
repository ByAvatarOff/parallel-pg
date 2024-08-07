FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update

RUN pip install "poetry==1.8.3"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root

COPY src .
