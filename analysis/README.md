## Native
1. Install `poetry` to manage dependencies. [Guide](https://python-poetry.org/docs/)
2. Install all the dependencies using `poetry install`
3. Download the english dictionary using `poetry run  python -m spacy download en_core_web_sm`
4. Run the `main.py` file using `poetry run python app/main.py`

## Docker
### [TODO]: Fix the download dictionary part
To build the image

```
docker build -t analysis .
```

To run it
```
docker run analysis:latest
```

