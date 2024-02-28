#!/bin/bash -eu

poetry config virtualenvs.path  ./local/django
poetry install
poetry run ./manage.py migrate

exec "$@"
