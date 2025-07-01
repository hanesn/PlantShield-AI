@echo off
setlocal

set DASHBOARDS_DIR=%~dp0..\dashboards

REM Check if network exists, create if not
docker network inspect ml-monitoring >nul 2>&1
if %errorlevel% neq 0 (
    echo Creating Docker network 'ml-monitoring'...
    docker network create ml-monitoring
)

docker compose -f "%DASHBOARDS_DIR%\docker-compose.yaml" up -d

echo Monitoring stack is up
endlocal
