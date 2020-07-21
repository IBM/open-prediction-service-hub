#!/usr/bin/env sh


set -e


# Load data in database
# shellcheck disable=SC1090
. "${OPS_HOME}"/prestart.sh


if [ ! -f "${MODEL_STORAGE}/key.pem" ] || [ ! -f "${MODEL_STORAGE}/cert.pem" ]; then
  # default certificate
  echo "[INFO] SSL certificates not found"
  echo "[INFO] Creating default certificates"
  openssl req \
    -x509 -newkey rsa:4096 -sha512 \
    -nodes \
    -subj '/CN=localhost' \
    -days 365 \
    -keyout "${MODEL_STORAGE}/key.pem" -out "${MODEL_STORAGE}/cert.pem"
fi



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
            --certfile="${MODEL_STORAGE}/cert.pem" \
            --keyfile="${MODEL_STORAGE}/key.pem" \
            main:app
