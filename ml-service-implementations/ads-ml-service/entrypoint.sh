#!/usr/bin/env sh


set -e


# Load data in database
# shellcheck disable=SC1090
. "${OPS_HOME}"/prestart.sh


if [ ! -f "${SSL_SETTINGS}/server.key" ] || [ ! -f "${SSL_SETTINGS}/server.crt" ] || [ ! -f "${SSL_SETTINGS}/ca.crt" ]; then
  # default certificate
  echo "[INFO] SSL certificates not found"
  echo "[INFO] Creating default certificates"
  openssl req \
    -x509 -newkey rsa:4096 -sha512 \
    -nodes \
    -subj '/CN=localhost' \
    -days 365 \
    -keyout "${SSL_SETTINGS}/server.key" -out "${SSL_SETTINGS}/server.crt"
  cp "${SSL_SETTINGS}/server.crt" "${SSL_SETTINGS}/ca.crt"
  echo "[INFO] Created self-signed certificates"
fi


# Default parameters:
#   Uvicorn worker class is required by Fastapi
exec gunicorn \
            --worker-class=uvicorn.workers.UvicornWorker \
            --config=file:gunicorn.init.py \
            "main:get_app()"
