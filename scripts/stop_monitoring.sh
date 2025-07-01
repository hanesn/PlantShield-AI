#!/bin/bash

DASHBOARDS_DIR="$(dirname "$0")/../dashboards"

docker compose -f "$DASHBOARDS_DIR/docker-compose.yaml" down
echo "Monitoring stack stopped"
