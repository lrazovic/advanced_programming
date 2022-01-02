FROM python:3.8-slim AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-dev

# ---

FROM python:3.8-slim
WORKDIR /app
COPY --from=builder /app /app
ADD . /app
EXPOSE 5000
CMD /app/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 5000