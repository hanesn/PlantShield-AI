#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")/.."

# Load .env variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^\s*$' | xargs)
else
    echo "[ERROR] .env file not found"
    exit 1
fi

if [ "$USE_TF_SERVING" = "True" ]; then
    echo "Starting TensorFlow Serving..."
    bash scripts/start_tf_serving.sh
else
    echo "USE_TF_SERVING=False - Skipping TensorFlow Serving startup"
fi

if [ "$ENABLE_METRICS" = "True" ]; then
    echo "Starting Prometheus and Grafana..."
    bash scripts/start_monitoring.sh
else
    echo "ENABLE_METRICS=False - Skipping monitoring stack startup"
fi

echo "Startup complete"