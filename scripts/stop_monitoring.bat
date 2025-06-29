@echo off
setlocal

set DASHBOARDS_DIR=%~dp0..\dashboards
docker compose -f "%DASHBOARDS_DIR%\docker-compose.yaml" down
echo Monitoring stack stopped
endlocal
