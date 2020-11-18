#!/usr/bin/env sh


set -e


# Load data in database
# shellcheck disable=SC1090
. "${OPS_HOME}"/prestart.sh


if [ ! -f "${SETTINGS}/server.key" ] || [ ! -f "${SETTINGS}/server.crt" ] || [ ! -f "${SETTINGS}/ca.crt" ]; then
  # default certificate
  echo "[INFO] SSL certificates not found"
  echo "[INFO] Creating default certificates"
  openssl req \
    -x509 -newkey rsa:4096 -sha512 \
    -nodes \
    -subj '/CN=localhost' \
    -days 365 \
    -keyout "${SETTINGS}/server.key" -out "${SETTINGS}/server.crt"
  cp "${SETTINGS}/server.crt" "${SETTINGS}/ca.crt"
  echo "[INFO] Created self-signed certificates"
fi


# Default parameters:
#   Uvicorn worker class is required by Fastapi
exec gunicorn \
            --worker-class=uvicorn.workers.UvicornWorker \
             --config=file:"${OPS_HOME}"/app/gunicorn.init.py \
            app.main:get_app()
