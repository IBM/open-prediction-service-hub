#!/usr/bin/env bash


set -o xtrace
set -o errexit
set -o nounset
set -o pipefail


YELLOW='\033[1;33m'
NC='\033[0m'


IMAGE_TAG="${DEPLOY_TIMESTAMP}-${TRAVIS_BUILD_NUMBER}-${TRAVIS_BRANCH//[\/]/-}"


install_ibm_cloud_cli() {
  echo "${YELLOW}[INFO] Installing CLI tools${NC}"
  curl -sL https://ibm.biz/idt-installer | bash
}

ibm_cloud_login() {
  echo "${YELLOW}[INFO] Authenticating ibm cloud${NC}"
  ibmcloud login -a https://api.ng.bluemix.net --apikey "${IBMCLOUD_API_KEY}"
}

ibm_container_registry_login() {
  echo "${YELLOW}[INFO] Authenticating ibm container registry${NC}"
  ibmcloud cr login
}

tag_image() {
  echo "${YELLOW}[INFO] Tagging image${NC}"
  docker tag open-prediction:"${IMAGE_TAG}" us.icr.io/"${CR_NAMESPACE}"/open-prediction:"${IMAGE_TAG}"
  docker tag open-prediction:latest us.icr.io/"${CR_NAMESPACE}"/open-prediction:latest
}

push_image() {
  echo "${YELLOW}[INFO] Pushing image${NC}"
  docker push us.icr.io/"${CR_NAMESPACE}"/open-prediction:"${IMAGE_TAG}"
  docker push us.icr.io/"${CR_NAMESPACE}"/open-prediction:latest
}

deploy() {
  echo "${YELLOW}[INFO] Begin deployment${NC}"
  install_ibm_cloud_cli
  ibm_cloud_login
  ibm_container_registry_login
  tag_image
  push_image
}

deploy
