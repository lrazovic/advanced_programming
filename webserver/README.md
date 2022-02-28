# Build

To build the image

```bash
docker build -t webserver .
```

## Run

### Prerequisites

* Valid `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in a `.env` file, in the same place where you find the `.env.example`

### Run via Docker

To run it

```bash
docker run -it -p 5000:5000 webserver
```

The webserver is live on: `http://0.0.0.0:5000/`, while the documentation is on `http://0.0.0.0:5000/docs`

### Run without Docker (FOR DEBUG ONLY)

* `poetry install`
* `env DEV=1 poetry run python app/main.py`

The webserver is live on: `http://0.0.0.0:8080/`, while the documentation is on `http://0.0.0.0:8080/docs`
