#!/usr/bin/env sh


set -e


# Load data in database
# shellcheck disable=SC1090
. "${OPS_HOME}"/prestart.sh

# Default parameters:
#   Uvicorn worker class is required by Fastapi
#   Container schedulers typically expect logs to come out on stdout/stderr, thus gunicorn is configured to do so
#   Gunicorn needs to store its temporary file in memory (e.g. /dev/shm)
# Start
exec gunicorn \
            --worker-class=uvicorn.workers.UvicornWorker \
            --log-file=- \
            --worker-tmp-dir=/dev/shm \
            --config=file:gunicorn.init.py \
            --bind=:8080 \
            main:app
