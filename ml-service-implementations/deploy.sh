#$!/bin/bash
SOURCE="${BASH_SOURCE[0]}"
DIR="$( dirname "$SOURCE" )"

DEPLOY_SERVICE=$1

cd ${DIR}/${DEPLOY_SERVICE}
docker build -t ${DEPLOY_SERVICE}:latest -f Dockerfile .
echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin "${DOCKER_REGISTRY_URL}"
docker tag ${DEPLOY_SERVICE}:latest "${DOCKER_REGISTRY_URL}/${DOCKER_NAMESPACE}/${DEPLOY_SERVICE}:${DEPLOY_TAG}" 
docker push "${DOCKER_REGISTRY_URL}/${DOCKER_NAMESPACE}/${DEPLOY_SERVICE}:${DEPLOY_TAG}" 