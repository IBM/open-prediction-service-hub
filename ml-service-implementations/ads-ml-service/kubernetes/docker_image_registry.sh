#!/usr/bin/env bash


set -o xtrace
set -o errexit
set -o nounset
set -o pipefail


YELLOW='\033[1;33m'
NC='\033[0m'

IMAGE_NAME="decisions-tooling/ads-ml-service"
IMAGE_TAG="${RELEASE_YEAR}${DESIGNER_COMPATIBLE_REL}"
IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"

login() {
  echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin "${REGISTRY_URL}"
}

tag_image() {
  docker tag ads-ml-service:latest "${REGISTRY_URL}/${IMAGE}"
}

push_image() {
  echo -e "${YELLOW}[INFO] Pushing image ${REGISTRY_URL}/${IMAGE}${NC}"
  docker push "${REGISTRY_URL}/${IMAGE}"
}


deploy() {
  login
  tag_image
  push_image
}

deploy
