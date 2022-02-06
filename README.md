# advanced_programming

Project for the "Laboratory of Advanced Programming" course 2021/2022

## Run using `docker compose`

```bash
docker compose up --build -d
```

You can check if the containers are running using:

```bash
docker ps
```

The frontend is now running on `http://localhost:3000` and the backend on `http://localhost:3000/api`

You can update a single service using

```bash
docker compose up -d --no-deps --build {service_name}
```

If we want to update the `view` service:

```bash
docker compose up -d --no-deps --build postgres
```

The services are:

* `view`
* `webserver`
* `postgres`
* `analysis`
* `fetcher`
* `authentication`
