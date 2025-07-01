#!/bin/bash
cd "$(dirname "$0")/.."

if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^\s*$' | xargs)
else
    echo "[ERROR] .env file not found"
    exit 1
fi

if [ "$USE_TF_SERVING" = "True" ]; then
    echo "Stopping TensorFlow Serving..."
    bash scripts/stop_tf_serving.sh
else
    echo "USE_TF_SERVING=False — Skipping TensorFlow Serving stop"
fi

if [ "$ENABLE_METRICS" = "True" ]; then
    echo "Stopping monitoring stack..."
    bash scripts/stop_monitoring.sh
else
    echo "ENABLE_METRICS=False — Skipping monitoring stop"
fi

echo "Shutdown complete"