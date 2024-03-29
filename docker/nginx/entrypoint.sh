#!/bin/sh

envsubst '$${BACKEND_HOST}:$${BACKEND_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
cat /etc/nginx/nginx.conf

exec "$@"
