#!/bin/bash -e
# Any commands which fail will cause the shell script to exit immediately
set -e

# Configure kubectl
kubectl config set-cluster kube-cluster --server=$KUBE_URL --insecure-skip-tls-verify
kubectl config set-credentials kube-cluster --token="$KUBE_TOKEN"
kubectl config set-context kube-cluster --cluster=kube-cluster --user=kube-cluster
kubectl config use-context kube-cluster