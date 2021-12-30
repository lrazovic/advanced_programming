FROM python:3.8-slim AS builder
EXPOSE 5000
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi

# ---

FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /app /app
ADD . /app