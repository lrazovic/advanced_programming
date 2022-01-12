# advanced_programming
Project for the "Laboratory of Advanced Programming" course 2021/2022

# Run using `docker compose`
```
$ docker compose up --build -d
```
You can check if the containers are running using:
```
$ docker ps
```
The frontend is now running on `http://localhost:3000` and the backend on `http://localhost:3000/api`

You can update a single service using
```
$ docker compose up -d --no-deps --build {service_name}
```
If we want to update the `view` service:
```
$ docker compose up -d --no-deps --build view
```
The services are:
* `view`
* `webserver`
* `mongodb`
* `analysis`
* `fether`
* Heavily WIP: `easyauth`