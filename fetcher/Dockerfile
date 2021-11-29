FROM python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

COPY . .

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.11

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

RUN . /venv/bin/activate && poetry install --no-dev --no-root

# RUN . /venv/bin/activate && poetry build

CMD ["python", "main.py"]