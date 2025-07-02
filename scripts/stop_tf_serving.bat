@echo off
set CONTAINER_NAME=tf_serving_container

docker stop %CONTAINER_NAME%
docker rm %CONTAINER_NAME%
echo Container stopped and removed
