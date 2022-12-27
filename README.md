# Test app Backend

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage](https://img.shields.io/badge/coverage-75%25-green)

## You can try it here
Swagger UI
```
http://159.89.100.196:8000/docs
```

Grafana Dashboard
```
http://159.89.100.196:3000/d/dLsDQIUnz/fastapi-observability
```


## Run project

You can run project by cloning from GitHub and run docker-compose

```
git clone git@github.com:Nerrow/testSidusApp.git

touch .env

#Fill by example from .env.example

docker compose --env-file ./.env up -d --build
```

## Docs and Metrics
Swagger UI
```
http://localhost:8000/docs
```

Redoc UI
```
http://localhost:8000/redoc
```

Grafana Dashboard
```
http://localhost:3000/d/dLsDQIUnz/fastapi-observability
```

## Run tests

```
docker compose exec app-user pytest . 
```

## Project structure

```
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── alembic.ini
│   ├── api
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── db
│   │   ├── db.py
│   │   ├── db_utils.py
│   │   └── migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions
│   ├── exceptions
│   │   ├── auth.py
│   │   └── user.py
│   ├── main.py
│   ├── models
│   │   ├── core.py
│   │   └── user.py
│   ├── repositories
│   │   ├── base.py
│   │   └── user.py
│   ├── schemas
│   │   ├── auth.py
│   │   └── user.py
│   ├── services
│   │   ├── auth.py
│   │   ├── cache.py
│   │   ├── user.py
│   │   └── utils.py
│   ├── settings.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_health.py
│   │   └── test_user.py
│   └── utils.py
├── docker-compose.yaml
├── etc
│   ├── dashboards
│   │   └── fastapi-observability.json
│   ├── dashboards.yaml
│   ├── grafana
│   │   └── datasource.yml
│   └── prometheus
│       └── prometheus.yml
└── req.txt
```
