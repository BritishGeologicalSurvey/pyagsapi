#!/bin/bash -e
# Any commands which fail will cause the shell script to exit immediately
set -e

# See the commands executed in the command window
set -x

# Change working directory to this script location
cd "$(dirname "$0")"

# Create a timestamp to inject into the deployment to force redeployment everytime
export DEPLOY_TIMESTAMP=`date +'%s'`

# Check deployment variables exist
if [[ -z $APP_HOSTNAME || -z $DEPLOY_IMAGE || -z $CONTAINER_PORT || -z $DOCKER_SECRET ]]; then
  echo 'one or more  deployment variables are undefined'
  exit 1
fi

# Check gitlab ci variables exist
if [[ -z $KUBE_NAMESPACE || -z $CI_PROJECT_PATH_SLUG || -z $CI_ENVIRONMENT_SLUG ]]; then
  echo 'one or more gitlab ci variables are undefined'
  exit 1
fi

# Check DMZ variables exist
if [ $CI_COMMIT_BRANCH = "staging-dmz" || $CI_COMMIT_BRANCH = "production-dmz" ]; then
  if [[ -z $DMZ_DOCKER_SECRET || -z $DMZ_REGISTRY_USER || -z $DMZ_REGISTRY_PASSWORD || -z $DMZ_REGISTRY ]]; then
    echo 'One or more DMZ variables are undefined'
    exit 1
  fi
fi

source ./kube-config.sh

# Create Namespace if it doesn't already exist
kubectl create namespace ${KUBE_NAMESPACE} || true

# Configure kubectl to use namespace
kubectl config set-context --current --namespace=${KUBE_NAMESPACE}

# Replace variables and Deploy config files
for f in manifests/*.yml ; do envsubst < "$f" | kubectl apply -f - ; done