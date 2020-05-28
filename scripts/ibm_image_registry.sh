#!/usr/bin/env bash


set -o xtrace
set -o errexit
set -o nounset
set -o pipefail


IMAGE_TAG="${DEPLOY_TIMESTAMP}-${TRAVIS_BUILD_NUMBER}-${TRAVIS_BRANCH//[\/]/-}"


install_ibm_cloud_cli() {
  curl -sL https://ibm.biz/idt-installer | bash
}

ibm_cloud_login() {
  ibmcloud login -a https://api.ng.bluemix.net --apikey "${IBMCLOUD_API_KEY}"
}

ibm_container_registry_login() {
  ibmcloud cr login
}

tag_image() {
  docker tag open-prediction:"${IMAGE_TAG}" us.icr.io/"${CR_NAMESPACE}"/open-prediction:"${IMAGE_TAG}"
  docker tag open-prediction:latest us.icr.io/"${CR_NAMESPACE}"/open-prediction:latest
}

push_image() {
  docker push us.icr.io/"${CR_NAMESPACE}"/open-prediction:"${IMAGE_TAG}"
  docker push us.icr.io/"${CR_NAMESPACE}"/open-prediction:latest
}

deploy() {
  install_ibm_cloud_cli
  ibm_cloud_login
  ibm_container_registry_login
  tag_image
  push_image
}

deploy
