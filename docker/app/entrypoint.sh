#!/bin/bash -eu

echo 'initialize'
poetry run ./manage.py migrate

exec "$@"
