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
  docker run --rm -it --user=1001:0 --entrypoint="venv/bin/python3" -e RETRAIN_MODELS=1 ads-ml-service:latest -m pytest -v app/tests
}

function launch_tls_configuration_testes() {
  local service_url_tls
  local service_url_mtls
  declare -i n=0

  chmod 555 "${__dir}/ads-ml-service-keys/server/tls.crt"
  chmod 555 "${__dir}/ads-ml-service-keys/server/tls.key"
  chmod 555 "${__dir}/ads-ml-service-keys/client/tls.crt"
  chmod 555 "${__dir}/ads-ml-service-keys/client/tls.key"

  docker \
    run --rm -d \
    -p 127.0.0.1:8081:8080 \
    --name ads-ml-service-tls \
    --user 1001:root \
    -e TLS_CRT=/etc/ads-ml-service/tls/tls.crt \
    -e TLS_KEY=/etc/ads-ml-service/tls/tls.key \
    -v "${__dir}/ads-ml-service-keys/server/tls.crt":/etc/ads-ml-service/tls/tls.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.key":/etc/ads-ml-service/tls/tls.key \
    ads-ml-service:latest

  docker \
    run --rm -d \
    -p 127.0.0.1:8082:8080 \
    --name ads-ml-service-mtls \
    --user 1001:0 \
    -e TLS_CRT=/etc/ads-ml-service/tls/tls.crt \
    -e TLS_KEY=/etc/ads-ml-service/tls/tls.key \
    -e CA_CRT=/etc/ads-ml-service/tls/ca.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.crt":/etc/ads-ml-service/tls/tls.crt \
    -v "${__dir}/ads-ml-service-keys/server/tls.key":/etc/ads-ml-service/tls/tls.key \
    -v "${__dir}/ads-ml-service-keys/client/tls.crt":/etc/ads-ml-service/tls/ca.crt \
    ads-ml-service:latest

  sleep 5
  docker ps -a
  docker logs --tail 20 ads-ml-service-tls

  service_url_tls="https://127.0.0.1:8081"
  service_url_mtls="https://127.0.0.1:8082"

  until ((n >= 60)); do
    test_tls_conn "${service_url_tls}" && break
    n=$((n + 1))
    echo "${service_url_tls}/info not available"
    sleep 10
  done
  if ! ((n < 60)); then
    echo "can not get ${service_url_tls}/info in 10 min"
    exit 1
  fi

  n=0
  until ((n >= 60)); do
    test_mtls_conn "${service_url_mtls}" && break
    n=$((n + 1))
    echo "${service_url_mtls}/info not available"
    sleep 10
  done
  if ! ((n < 60)); then
    echo "can not get ${service_url_mtls}/info in 10 min"
    exit 1
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

function test_mtls_conn() {
  local service_url_mtls=$1

  local resp_mtls
  local status_mtls

  echo "Testing mTls connection ${service_url_mtls}"

  resp_mtls=$(curl -s \
    --cacert "${__dir}"/ads-ml-service-keys/server/tls.crt \
    --key "${__dir}"/ads-ml-service-keys/client/tls.key \
    --cert "${__dir}"/ads-ml-service-keys/client/tls.crt \
    -H "Accept: application/json" -H "Content-Type: application/json" "${service_url_mtls}/info")

  status_mtls=$(jq -r '.status' <<<"${resp_mtls}")

  if ! [ "$status_mtls" == "ok" ]; then
    return 1
  fi
}

function test_tls_conn() {
  local service_url_tls=$1

  local status_tls
  local resp_tls

  echo "Testing Tls connection ${service_url_tls}"

  resp_tls=$(curl -s \
    --cacert "${__dir}"/ads-ml-service-keys/server/tls.crt \
    -H "Accept: application/json" -H "Content-Type: application/json" "${service_url_tls}/info")
  status_tls=$(jq -r '.status' <<<"${resp_tls}")
  if ! [ "$status_tls" == "ok" ]; then
    return 1
  fi
}

gen_crts
prepare_env
launch_unit_testes
launch_tls_configuration_testes
