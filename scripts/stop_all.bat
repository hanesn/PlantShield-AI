@echo off
cd /d "%~dp0\.."

REM Load .env variables
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    set "%%A=%%B"
)

REM Stop TensorFlow Serving if enabled
if /i "%USE_TF_SERVING%"=="True" (
    echo Stopping TensorFlow Serving...
    call scripts\stop_tf_serving.bat
) else (
    echo USE_TF_SERVING is False — Skipping TF Serving stop
)

REM Stop Prometheus & Grafana if enabled
if /i "%ENABLE_METRICS%"=="True" (
    echo Stopping monitoring stack...
    call scripts\stop_monitoring.bat
) else (
    echo ENABLE_METRICS is False — Skipping monitoring stop
)

echo Shutdown complete