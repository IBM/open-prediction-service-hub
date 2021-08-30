#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$(cd "$(dirname "${__dir}")" && pwd)"

function prepare_env() {
  docker build -t ads-ml-service:latest "${__root}"
}

function launch_unit_testes() {
  echo "Launching unit test"
  docker run --rm -it --entrypoint="venv/bin/python3" -e RETRAIN_MODELS=1 ads-ml-service:latest -m pytest -v app/tests
}

function launch_tls_configuration_testes() {
  echo "Test Tls and mTls connection"
  local service_url_tls
  local service_url_mtls
  local resp_tls
  local resp_mtls
  local status_tls
  local status_mtls

  docker \
    run --rm -d \
    -p 8080:8080 \
    --name ads-ml-service-tls \
    -e TLS_CRT=/etc/ads-ml-service/tls/tls.crt \
    -e TLS_KEY=/etc/ads-ml-service/tls/tls.key \
    -v "${__dir}/ads-ml-service-keys/server/tls.crt":/etc/ads-ml-service/tls/tls.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.key":/etc/ads-ml-service/tls/tls.key \
    ads-ml-service:latest

  docker \
    run --rm -d \
    -p 8081:8080 \
    --name ads-ml-service-mtls \
    -e TLS_CRT=/etc/ads-ml-service/tls/tls.crt \
    -e TLS_KEY=/etc/ads-ml-service/tls/tls.key \
    -e CA_CRT=/etc/ads-ml-service/tls/ca.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.crt":/etc/ads-ml-service/tls/tls.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.key":/etc/ads-ml-service/tls/tls.key \
    -v "${__dir}/ads-ml-service-keys/client/tls.crt":/etc/ads-ml-service/tls/ca.crt \
    ads-ml-service:latest

  sleep 30
  service_url_tls="https://127.0.0.1:8080"
  service_url_mtls="https://127.0.0.1:8081"

  resp_tls=$(curl -s \
    --cacert "${__dir}"/ads-ml-service-keys/server/tls.crt \
    -H "Accept: application/json" -H "Content-Type: application/json" "${service_url_tls}/info")
  resp_mtls=$(curl -s \
    --cacert "${__dir}"/ads-ml-service-keys/server/tls.crt \
    --key "${__dir}"/ads-ml-service-keys/client/tls.key \
    --cert "${__dir}"/ads-ml-service-keys/client/tls.crt \
    -H "Accept: application/json" -H "Content-Type: application/json" "${service_url_mtls}/info")
  status_tls=$(jq -r '.status' <<<"${resp_tls}")
  status_mtls=$(jq -r '.status' <<<"${resp_mtls}")
  if ! [ "$status_tls" == "ok" ]; then
    return 1
  fi
  if ! [ "$status_mtls" == "ok" ]; then
    return 1
  fi
  echo "passed"

  docker stop ads-ml-service-tls
  docker stop ads-ml-service-mtls
}

function gen_crts() {
  mkdir -p "${__dir}"/ads-ml-service-keys/server
  mkdir -p "${__dir}"/ads-ml-service-keys/client
  openssl req -x509 -newkey rsa:4096 -sha256 -nodes \
    -subj '/CN=ads-ml-service.ads-ml-service.svc.cluster.local' \
    -addext "subjectAltName = DNS:ads-ml-service,DNS:ads-ml-service.ads-ml-service.svc.cluster.local,DNS:localhost,IP:0.0.0.0,IP:127.0.0.1" \
    -out "${__dir}"/ads-ml-service-keys/server/tls.crt \
    -keyout "${__dir}"/ads-ml-service-keys/server/tls.key
  openssl req -x509 -newkey rsa:4096 -sha256 -nodes \
    -subj '/CN=localhost' \
    -addext "subjectAltName = DNS:localhost" \
    -out "${__dir}"/ads-ml-service-keys/client/tls.crt \
    -keyout "${__dir}"/ads-ml-service-keys/client/tls.key
}

gen_crts
prepare_env
launch_unit_testes
launch_tls_configuration_testes
