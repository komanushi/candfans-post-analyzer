#!/bin/bash -eu

poetry run ./manage.py migrate
poetry run ./manage.py schedule
poetry run gunicorn -- --config ./application/gunicorn_conf.py application.asgi:application
