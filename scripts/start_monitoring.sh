#!/bin/bash

DASHBOARDS_DIR="$(dirname "$0")/../dashboards"

# Ensure the external Docker network exists
if ! docker network inspect ml-monitoring >/dev/null 2>&1; then
    echo "Creating Docker network 'ml-monitoring'..."
    docker network create ml-monitoring
fi

docker compose -f "$DASHBOARDS_DIR/docker-compose.yaml" up -d

echo "Monitoring stack is up."
