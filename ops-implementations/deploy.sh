#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEPLOY_SERVICE=$1
DEPLOY_VERSION=$2

function trace_deploy() {
  echo "Deployment environment:"
  echo "TRAVIS_BRANCH=${TRAVIS_BRANCH:-not-set}"
  echo "TRAVIS_EVENT_TYPE=${TRAVIS_EVENT_TYPE:-not-set}"
  echo "TRAVIS_PULL_REQUEST=${TRAVIS_PULL_REQUEST:-not-set}"
  echo "TRAVIS_TAG=${TRAVIS_TAG:-not-set}"
  echo "TRAVIS_COMMIT=${TRAVIS_COMMIT:-not-set}"
}

function deploy() {
  local project_name=$1
  local project_ver=$2
  local artifactory_url=$3
  local artifactory_namespace=$4
  local repository_name=$5
  local artifactory_username=$6
  local artifactory_passwd=$7
  local branch_name=$8
  local tag_name=$9

  local deploy_tag
  if [ "${branch_name}" == "develop" ]; then
    local build_time
    build_time=$(date -u +'%y%m%d-%H%M%S-0000')
    deploy_tag="${project_ver}-snapshot-${build_time}"
  elif [ "${branch_name}" == "main" ]; then
    deploy_tag="${project_ver}"
  elif [ "${tag_name}" != "not-set" ]; then
    deploy_tag="${tag_name}"
  else
    echo "branch not in (develop, main) and is not tag build"
    exit 1
  fi
  echo "deploy_tag=${deploy_tag}"

  # Build project
  docker build -t "${repository_name}":latest "${__dir}/${project_name}"
  # Docker login
  echo "${artifactory_passwd}" | docker login -u "${artifactory_username}" --password-stdin "${artifactory_url}"

  docker tag "${repository_name}":latest "${artifactory_url}/${artifactory_namespace}/${repository_name}:${deploy_tag}"
  docker push "${artifactory_url}/${artifactory_namespace}/${repository_name}:${deploy_tag}"

  # Update stable & latest tag
  if [ "${branch_name}" == "main" ]; then
    docker tag "${repository_name}":latest "${artifactory_url}/${artifactory_namespace}/${repository_name}:stable"
    docker push "${artifactory_url}/${artifactory_namespace}/${repository_name}:stable"
  fi
  if [ "${branch_name}" == "develop" ]; then
    docker tag "${repository_name}":latest "${artifactory_url}/${artifactory_namespace}/${repository_name}:latest"
    docker push "${artifactory_url}/${artifactory_namespace}/${repository_name}:latest"
  fi
}

if [[ -z "${DOCKER_REGISTRY_URL+x}" ]]; then
  echo "DOCKER_REGISTRY_URL not set can't deploy"
  exit 0
fi

if [[ -z "${DOCKER_NAMESPACE+x}" ]]; then
  echo "DOCKER_NAMESPACE not set can't deploy"
  exit 0
fi

if [[ -z "${DOCKER_USERNAME+x}" ]]; then
  echo "DOCKER_USERNAME not set can't deploy"
  exit 0
fi

if [[ -z "${DOCKER_PASSWORD+x}" ]]; then
  echo "DOCKER_PASSWORD not set can't deploy"
  exit 0
fi

trace_deploy
deploy \
  "${DEPLOY_SERVICE}" \
  "${DEPLOY_VERSION}" \
  "${DOCKER_REGISTRY_URL}" \
  "${DOCKER_NAMESPACE}" \
  "${DEPLOY_SERVICE}" \
  "${DOCKER_USERNAME}" \
  "${DOCKER_PASSWORD}" \
  "${TRAVIS_BRANCH:-not-set}" \
  "${TRAVIS_TAG:-not-set}"
