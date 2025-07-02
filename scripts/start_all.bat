@echo off
REM Navigate to root dir from scripts/
cd /d "%~dp0\.."

REM Load .env variables
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    set "%%A=%%B"
)

REM Start TensorFlow Serving only if enabled
if /i "%USE_TF_SERVING%"=="True" (
    echo Starting TensorFlow Serving...
    call scripts\start_tf_serving.bat
) else (
    echo USE_TF_SERVING is False - Skipping TF Serving startup
)

REM Start Prometheus + Grafana only if enabled
if /i "%ENABLE_METRICS%"=="True" (
    echo Starting monitoring stack...
    call scripts\start_monitoring.bat
) else (
    echo ENABLE_METRICS is False - Skipping monitoring startup
)

echo Startup complete