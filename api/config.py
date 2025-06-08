import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

USE_TF_SERVING = os.getenv("USE_TF_SERVING", "False") == "True"
MODEL_DIR = os.getenv("MODEL_DIR", "saved_models")
MODEL_PATTERN = os.getenv("MODEL_PATTERN", "tomato_model-v*.keras")
TF_SERVING_URL = os.getenv("TF_SERVING_URL", "http://localhost:8501/v1/models/potatoes_model:predict")
LOG_FILE = os.getenv("LOG_FILE", "logs/api.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
