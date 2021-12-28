# From: https://stackoverflow.com/a/64642121
# Extra info: https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi

FROM python:3.8-slim
EXPOSE 5000

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

COPY . .

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# RUN poetry build

COPY ./app /code/app