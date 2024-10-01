# SWA: Sweetwest Airlines
This repo contains the software infrastructure for our 2024 Halloween project.

## Setup
1. Install [poetry](https://python-poetry.org/docs/).
2. Run `poetry install --no-root` in the top-level project directory.
    - You can run `poetry config virtualenvs.in-project true` to keep your .venv within the project.
3. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
4. Run `npm install`.

## Running
1. Run `poetry run pip freeze > requirements.txt` so that the Docker containers will be able to install the current dependencies.
2. Use .env.sample as a reference to create and populate an `.env.dev` file.
3. Run `docker compose -f .\compose.dev.yml up --build -d`.
4. Run `docker compose -f .\compose.dev.yml exec django python manage.py migrate` to set up your database.

## Testing
1. Run `poetry run pytest` to run Python tests.
