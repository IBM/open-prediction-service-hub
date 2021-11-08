#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

. "${OPS_HOME}"/prestart.sh

function main() {
  local proxy_host
  local http_port
  declare -i workers

  proxy_host="${HOST:-0.0.0.0}"
  http_port="${HTTP_PORT:-8080}"
  https_port="${HTTPS_PORT:-8443}"
  if [[ -v WEB_CONCURRENCY ]]; then
    workers="${WEB_CONCURRENCY}"
  elif [[ -v GUNICORN_WORKER_NUM ]]; then
    echo "GUNICORN_WORKER_NUM is deprecated in favour of WEB_CONCURRENCY"
    workers="${GUNICORN_WORKER_NUM}"
  else
    workers=2
  fi
  echo "worker_num=${workers}"

  if [[ -v TLS_CRT ]] && [[ -v TLS_KEY ]] && [[ -v CA_CRT ]]; then
    echo "launching service with mTLS"
    launch_mtls "${proxy_host}" "${http_port}" "${https_port}" "${workers}" "${TLS_CRT}" "${TLS_KEY}" "${CA_CRT}"
  elif [[ -v TLS_CRT ]] && [[ -v TLS_KEY ]] && [[ ! -v CA_CRT ]]; then
    echo "launching service with TLS"
    launch_tls "${proxy_host}" "${http_port}" "${https_port}" "${workers}" "${TLS_CRT}" "${TLS_KEY}"
  else
    echo "launching service without TLS"
    launch_without_tls "${proxy_host}" "${http_port}" "${workers}"
  fi
}

function launch_mtls() {
  local host=$1
  local http_port=$2
  local https_port=$3
  declare -i workers=$4
  local tls_crt=$5
  local tls_key=$6
  local ca_crt=$7

  exec \
    hypercorn \
    --insecure-bind "${host}:${http_port}" \
    --bind "${host}:${https_port}" \
    --workers "${workers}" \
    --certfile "${tls_crt}" \
    --keyfile "${tls_key}" \
    --ca-certs "${ca_crt}" \
    --verify-mode CERT_REQUIRED \
    'app.main:get_app()'
}

function launch_tls() {
  local host=$1
  local http_port=$2
  local https_port=$3
  declare -i workers=$4
  local tls_crt=$5
  local tls_key=$6

  exec \
    hypercorn \
    --insecure-bind "${host}:${http_port}" \
    --bind "${host}:${https_port}" \
    --workers "${workers}" \
    --certfile "${tls_crt}" \
    --keyfile "${tls_key}" \
    'app.main:get_app()'
}

function launch_without_tls() {
  local host=$1
  local port=$2
  declare -i workers=$3

  exec \
    hypercorn \
    --bind "${host}:${port}" \
    --workers "${workers}" \
    'app.main:get_app()'
}

main
