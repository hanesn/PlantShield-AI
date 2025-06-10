import subprocess
import time
import requests
import pytest
import os
import signal
import sys

def get_creation_flags():
    if os.name == "nt":
        return subprocess.CREATE_NEW_PROCESS_GROUP
    return 0

@pytest.fixture(scope="session", autouse=True)
def start_server():
    # Start FastAPI server as subprocess
    server = subprocess.Popen(
        ["python", "-m", "api.main"], 
        stdout=sys.stdout,
        stderr=sys.stderr,
        creationflags=get_creation_flags()
    )

    # Wait until server is live
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            res = requests.get("http://localhost:8000/health")
            if res.status_code in [200, 503]:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    else:
        server.terminate()
        raise RuntimeError("FastAPI server didn't start in time")

    yield

    # Teardown
    if os.name == "nt":
        server.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        server.terminate()
    server.wait()
