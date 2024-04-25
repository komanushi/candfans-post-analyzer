#!/bin/bash -eu

poetry run ./manage.py migrate
poetry run python ./manage.py rqscheduler default &
poetry run python ./manage.py rqworker default

