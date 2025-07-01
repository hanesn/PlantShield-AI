#!/bin/bash

CONTAINER_NAME=tf_serving_container

docker stop $CONTAINER_NAME >/dev/null 2>&1 || echo "Container not running"
docker rm $CONTAINER_NAME >/dev/null 2>&1 || echo "Container not found"
echo "Container stopped and removed"