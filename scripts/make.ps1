param (
    [string]$task = ""
)

# Move to project root
Set-Location "$PSScriptRoot\.."

# Load .env variables into environment
Get-Content ".env" | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]+)=(.+)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $value)
    }
}

$USE_TF_SERVING = $env:USE_TF_SERVING
$ENABLE_METRICS = $env:ENABLE_METRICS

switch ($task) {
    "start" {
        if ($USE_TF_SERVING -eq "True") {
            Write-Host "Starting TensorFlow Serving..."
            & scripts\start_tf_serving.bat
        } else {
            Write-Host "USE_TF_SERVING=False - Skipping TF Serving startup"
        }

        if ($ENABLE_METRICS -eq "True") {
            Write-Host "Starting Prometheus + Grafana..."
            & scripts\start_monitoring.bat
        } else {
            Write-Host "ENABLE_METRICS=False - Skipping monitoring startup"
        }
    }

    "stop" {
        if ($USE_TF_SERVING -eq "True") {
            Write-Host "Stopping TensorFlow Serving..."
            & scripts\stop_tf_serving.bat
        } else {
            Write-Host "USE_TF_SERVING=False - Skipping TF Serving stop"
        }

        if ($ENABLE_METRICS -eq "True") {
            Write-Host "Stopping monitoring stack..."
            & scripts\stop_monitoring.bat
        } else {
            Write-Host "ENABLE_METRICS=False - Skipping monitoring stop"
        }
    }

    "start-tf" { & scripts\start_tf_serving.bat }
    "stop-tf"  { & scripts\stop_tf_serving.bat }
    "start-monitoring" { & scripts\start_monitoring.bat }
    "stop-monitoring"  { & scripts\stop_monitoring.bat }

    "test-unit" {
        Write-Host "Running unit tests..."
        & pytest tests\unit
    }

    "test-integration" {
        Write-Host "Running integration tests..."
        & pytest tests\integration
    }

    "package" {
        Write-Host "Generating deployable package..."
        & python installer\package_project.py
    }

    Default {
        Write-Host "Invalid or no task provided."
        Write-Host "Available tasks:"
        Write-Host "  start               # Start all services"
        Write-Host "  stop                # Stop all services"
        Write-Host "  start-tf            # Start TensorFlow Serving only"
        Write-Host "  stop-tf             # Stop TensorFlow Serving only"
        Write-Host "  start-monitoring    # Start Prometheus + Grafana"
        Write-Host "  stop-monitoring     # Stop Prometheus + Grafana"
        Write-Host "  test-unit           # Run unit tests"
        Write-Host "  test-integration    # Run integration tests"
        Write-Host "  package             # Create ZIP archive of the project"
    }
}
