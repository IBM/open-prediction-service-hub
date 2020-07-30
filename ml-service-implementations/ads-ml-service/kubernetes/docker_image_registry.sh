#!/usr/bin/env bash


set -o xtrace
set -o errexit
set -o nounset
set -o pipefail


YELLOW='\033[1;33m'
NC='\033[0m'

# Required EN vars:
#   REGISTRY_URL
#   DOCKER_NAMESPACE
#   FULL_TAG: offered by .travis
DOCKER_REPOSITORY=${DOCKER_REPOSITORY:-"ads-ml-service"}
DOCKER_TAG=${DOCKER_TAG:-"${RELEASE_YEAR}${DESIGNER_COMPATIBLE_REL}"}

login() {
  echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin "${REGISTRY_URL}"
}

tag_image() {
  docker tag ads-ml-service:latest "${REGISTRY_URL}/${DOCKER_NAMESPACE}/${DOCKER_REPOSITORY}:${DOCKER_TAG}"
  docker tag ads-ml-service:latest "${REGISTRY_URL}/${DOCKER_NAMESPACE}/${DOCKER_REPOSITORY}:${FULL_TAG}"
}

push_image() {
  echo -e "${YELLOW}[INFO] Pushing image for repo: ${REGISTRY_URL}/${DOCKER_NAMESPACE}/${DOCKER_REPOSITORY}${NC}"
  docker push "${REGISTRY_URL}/${DOCKER_NAMESPACE}/${DOCKER_REPOSITORY}:${DOCKER_TAG}"
  docker push "${REGISTRY_URL}/${DOCKER_NAMESPACE}/${DOCKER_REPOSITORY}:${FULL_TAG}"
}


deploy() {
  login
  tag_image
  push_image
}

deploy
