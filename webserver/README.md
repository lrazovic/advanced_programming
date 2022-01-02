To build the image

```
docker build -t webserver .
```

To run it
```
docker run -it -p 5000:5000 webserver
```
The webserver is live on: `http://0.0.0.0:5000/`, while the documentation is on `http://0.0.0.0:5000/docs`