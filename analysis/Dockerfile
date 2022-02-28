FROM python:3.9-slim AS builder
WORKDIR /app
COPY  pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry==1.1.13
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-ansi --no-dev

# ---

FROM python:3.9-slim
EXPOSE 5001
WORKDIR /app
COPY --from=builder /app /app
COPY  . /app
RUN /app/.venv/bin/python -m nltk.downloader popular
CMD ["/app/.venv/bin/python", "app/main.py"]