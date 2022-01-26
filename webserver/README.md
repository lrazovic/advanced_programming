# Build

To build the image

```bash
docker build -t webserver .
```

To run it

```bash
docker run -it -p 5000:5000 webserver
```

The webserver is live on: `http://0.0.0.0:5000/`, while the documentation is on `http://0.0.0.0:5000/docs`

## Run without docker (currently unsupported, expect chaos)

* `poetry install`
* `env DEV=1 poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080`
