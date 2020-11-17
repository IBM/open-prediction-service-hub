#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

install_jre() {
  apt-get -qq update
  mkdir -p /usr/share/man/man1
  apt-get -qq install --assume-yes default-jre-headless
  rm -rf /var/lib/apt/lists/*
}

install_PyPMML() {
  python3 -m pip install --no-cache-dir --use-feature=2020-resolver pypmml~=0.9.7
  # python3 -m pip install --no-cache-dir --use-feature=2020-resolver nyoka~=4.3.0  # Used for testes
}

install_jre
install_PyPMML
