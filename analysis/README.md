# Run

## Native

```bash
poetry install
poetry run python app/main.py
```

## Docker

To build the image

```bash
docker build -t ap-analysis .
```

To run it

```bash
docker run -it -p 5001:5001 ap-analysis:latest
```
