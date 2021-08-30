#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

. "${OPS_HOME}"/prestart.sh

function main() {
  local proxy_host
  local proxy_port
  declare -i workers

  proxy_host="${HOST:-0.0.0.0}"
  proxy_port="${PORT:-8080}"
  if [[ -v WORKERS ]]; then
    workers="${WORKERS}"
  elif [[ -v GUNICORN_WORKER_NUM ]]; then
    workers="${GUNICORN_WORKER_NUM}"
  else
    workers=1
  fi
  echo "worker_num=${workers}"

  if [[ -v TLS_CRT ]] && [[ -v TLS_KEY ]] && [[ -v CA_CRT ]]; then
    echo "launching service with mTLS"
    launch_mtls "${proxy_host}" "${proxy_port}" "${workers}" "${TLS_CRT}" "${TLS_KEY}" "${CA_CRT}"
  elif [[ -v TLS_CRT ]] && [[ -v TLS_KEY ]] && [[ ! -v CA_CRT ]]; then
    echo "launching service with TLS"
    launch_tls "${proxy_host}" "${proxy_port}" "${workers}" "${TLS_CRT}" "${TLS_KEY}"
  else
    echo "launching service without TLS"
    launch_without_tls "${proxy_host}" "${proxy_port}" "${workers}"
  fi
}

function launch_mtls() {
  local host=$1
  local port=$2
  declare -i workers=$3
  local tls_crt=$4
  local tls_key=$5
  local ca_crt=$6

  exec \
    uvicorn \
    --factory app.main:get_app \
    --host "${host}" \
    --port "${port}" \
    --workers "${workers}" \
    --ssl-certfile "${tls_crt}" \
    --ssl-keyfile "${tls_key}" \
    --ssl-ca-certs "${ca_crt}" \
    --ssl-cert-reqs 1
}

function launch_tls() {
  local host=$1
  local port=$2
  declare -i workers=$3
  local tls_crt=$4
  local tls_key=$5

  exec \
    uvicorn \
    --factory app.main:get_app \
    --host "${host}" \
    --port "${port}" \
    --workers "${workers}" \
    --ssl-certfile "${tls_crt}" \
    --ssl-keyfile "${tls_key}"
}

function launch_without_tls() {
  local host=$1
  local port=$2
  declare -i workers=$3

  exec \
    uvicorn \
    --factory app.main:get_app \
    --host "${host}" \
    --port "${port}" \
    --workers "${workers}"
}

main
