import os
from api.config import USE_TF_SERVING, MODEL_DIR, MODEL_PATTERN, TF_SERVING_URL

def test_env_config_loaded():
    assert isinstance(USE_TF_SERVING, bool)
    assert isinstance(MODEL_DIR, str)
    assert isinstance(MODEL_PATTERN, str)
    assert isinstance(TF_SERVING_URL, str)

    # Optional: Check specific expected values if you want
    assert MODEL_DIR == os.getenv("MODEL_DIR", "saved_models")
    assert TF_SERVING_URL.startswith("http://")
