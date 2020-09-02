#!/usr/bin/env bash


set -o xtrace
set -o errexit
set -o nounset
set -o pipefail


YELLOW='\033[1;33m'
NC='\033[0m'


IMAGE_TAG="${DEPLOY_TIMESTAMP}-${TRAVIS_BUILD_NUMBER}-${TRAVIS_BRANCH//[\/]/-}"


install_ibm_cloud_cli() {
  echo -e "${YELLOW}[INFO] Installing CLI tools${NC}"
  curl -sL https://ibm.biz/idt-installer | bash
}

ibm_cloud_login() {
  echo -e "${YELLOW}[INFO] Authenticating ibm cloud${NC}"
  ibmcloud login -a https://api.ng.bluemix.net --apikey "${IBMCLOUD_API_KEY}"
}

ibm_container_registry_login() {
  echo -e "${YELLOW}[INFO] Authenticating ibm container registry${NC}"
  ibmcloud cr login
}

tag_image() {
  echo -e "${YELLOW}[INFO] Tagging image${NC}"
  docker tag ads-ml-service:"${IMAGE_TAG}" us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:"${IMAGE_TAG}"
  docker tag ads-ml-service:latest us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:latest
}

push_image() {
  echo -e "${YELLOW}[INFO] Pushing image${NC}"
  docker push us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:"${IMAGE_TAG}"
  docker push us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:latest
}

ibm_cloud_specific(){
  # Free version of register have limited size
  ibmcloud cr image-rm us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:latest || echo -e "Not need to remove image"
  ibmcloud cr build \
    -t us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:"${IMAGE_TAG}" \
    -t us.icr.io/"${CR_NAMESPACE}"/ads-ml-service:latest \
    -f Dockerfile .
}

deploy() {
  echo -e "${YELLOW}[INFO] Begin deployment${NC}"
  install_ibm_cloud_cli
  ibm_cloud_login
  ibm_container_registry_login
  # tag_image
  # push_image
  # images in free registry cannot surpass 500MB except build by ibmcloud tools
  ibm_cloud_specific
}

deploy
