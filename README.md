# rabbit_backend

## Ссылки
- [frontend](https://gitlab.aigang.ru/ai-gang/rabbit_frontend)
- [youtrack](https://youtrack.aigang.ru/agiles/158-2/current)
- [wiki](https://docs.aigang.ru/shelves/ai-gang)

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m rabbit_backend
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "rabbit_backend"
rabbit_backend
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "RABBIT_BACKEND_" prefix.

For example if you see in your "rabbit_backend/settings.py" a variable named like
`random_parameter`, you should provide the "RABBIT_BACKEND_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `rabbit_backend.settings.Settings.Config`.

An example of .env file:
```bash
RABBIT_BACKEND_RELOAD="True"
RABBIT_BACKEND_PORT="8000"
RABBIT_BACKEND_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/

## Remove DB
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --project-directory . rm -v
```

## Migrations

If you want to migrate your database, you should run following commands:
```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:
```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:
```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```bash
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=rabbit_backend" -e "POSTGRES_USER=rabbit_backend" -e "POSTGRES_DB=rabbit_backend" postgres:13.8-bullseye
```


2. Run the pytest.
```bash
pytest -vv .
```
