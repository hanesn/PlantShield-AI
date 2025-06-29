# Project Makefile for managing model serving and monitoring

.DEFAULT_GOAL := help

help:
	@echo "Available Make tasks:"
	@echo "  make start              - Start TF Serving & monitoring (based on .env)"
	@echo "  make stop               - Stop everything (based on .env)"
	@echo "  make start-tf           - Start only TensorFlow Serving"
	@echo "  make stop-tf            - Stop TensorFlow Serving"
	@echo "  make start-monitoring   - Start Prometheus + Grafana"
	@echo "  make stop-monitoring    - Stop Prometheus + Grafana"
	@echo "  make test-unit          - Run unit tests"
	@echo "  make test-integration   - Run integration tests"
	@echo "  make package            - Create ZIP archive of the project"

.PHONY: help start stop start-tf stop-tf start-monitoring stop-monitoring test-unit test-integration package

# Load .env
include .env
export

start:
ifeq ($(USE_TF_SERVING),True)
	@echo "Starting TensorFlow Serving..."
	bash scripts/start_tf_serving.sh
else
	@echo "USE_TF_SERVING=False - Skipping TF Serving startup"
endif

ifeq ($(ENABLE_METRICS),True)
	@echo "Starting Monitoring (Prometheus + Grafana)..."
	bash scripts/start_monitoring.sh
else
	@echo "ENABLE_METRICS=False - Skipping monitoring startup"
endif

stop:
ifeq ($(USE_TF_SERVING),True)
	@echo "Stopping TensorFlow Serving..."
	bash scripts/stop_tf_serving.sh
else
	@echo "USE_TF_SERVING=False - Skipping TF Serving stop"
endif

ifeq ($(ENABLE_METRICS),True)
	@echo "Stopping Monitoring stack..."
	bash scripts/stop_monitoring.sh
else
	@echo "ENABLE_METRICS=False - Skipping monitoring stop"
endif

start-tf:
	bash scripts/start_tf_serving.sh

stop-tf:
	bash scripts/stop_tf_serving.sh

start-monitoring:
	bash scripts/start_monitoring.sh

stop-monitoring:
	bash scripts/stop_monitoring.sh

test-unit:
	@echo "Running unit tests..."
	pytest tests/unit

test-integration:
	@echo "Running integration tests..."
	pytest tests/integration

package:
	@echo "Generating deployable package..."
	python installer/package_project.py