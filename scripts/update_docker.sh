#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

# Use the latest version of docker builder
function update_docker() {
  # https://docs.docker.com/engine/install/ubuntu/
  sudo apt-get update
  sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
  sudo apt-get update
  sudo apt-get -y -o Dpkg::Options::="--force-confnew" install docker-ce docker-ce-cli containerd.io

  sudo systemctl restart docker
  sudo chgrp travis /var/run/docker.sock
  sudo cp /usr/bin/docker /usr/local/bin/docker

  echo "Docker version:"
  docker version
  echo "Docker buildx version:"
  docker buildx version
}

update_docker
