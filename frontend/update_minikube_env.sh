#!/bin/bash

ENV_FILE="./.env.minikube"
MINIKUBE_IP=$(minikube ip)

if [ -z "$MINIKUBE_IP" ]; then
  echo "Failed to get Minikube IP. Is Minikube running?"
  exit 1
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  sed -i '' -E "s|^REACT_APP_API_URL=.*|REACT_APP_API_URL=http://${MINIKUBE_IP}:30080/predict|" $ENV_FILE
else
  # Linux / WSL
  sed -i -E "s|^REACT_APP_API_URL=.*|REACT_APP_API_URL=http://${MINIKUBE_IP}:30080/predict|" $ENV_FILE
fi

echo "Updated REACT_APP_API_URL to http://${MINIKUBE_IP}:30080/predict in $ENV_FILE"