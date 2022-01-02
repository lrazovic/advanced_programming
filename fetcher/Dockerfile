FROM python:3.8-slim AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-dev

# ---

FROM python:3.8-slim
EXPOSE 5002
WORKDIR /app
COPY --from=builder /app /app
ADD . /app
CMD /app/.venv/bin/python app/main.py