FROM python:3.9-slim as requirements-stage
WORKDIR /tmp
RUN pip install --no-cache-dir poetry==1.1.13
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["python", "app/main.py"]