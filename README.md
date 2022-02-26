# Laboratory of Advanced Programming

Project for the "Laboratory of Advanced Programming" course 2021/2022

## Run using `docker compose`

### Prerequisites

1. Docker
2. Docker Compose v2
3. A Google Client Secret/ID for oAuth (obtainable from [here](https://console.developers.google.com/apis)) as environments variables. You should put your secrets in a `.env` file in `webserver\app\.env` where the `.env.example` is located.

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
  