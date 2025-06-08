from fastapi import FastAPI,UploadFile,HTTPException
from utils import *
from config import USE_TF_SERVING
from pydantic import BaseModel
import logging
import uvicorn
import time
import requests
import os

if USE_TF_SERVING:
    from model_tf_serving import predict_tf_serving as predict_model
else:
    from model_local import predict_local as predict_model

Path("api/logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api/logs/api.log"),
        logging.StreamHandler()  # also keeps logging to terminal
    ]
)

app = FastAPI()
latest_model_file = get_latest_model_path()

class PredictionResponse(BaseModel):
    Class: str
    Confidence: float

@app.get("/")
async def ping():
    return "hello"

@app.get("/health")
async def health():
    logging.debug("/health endpoint called")
    if USE_TF_SERVING:
        try:
            res = requests.get("http://localhost:8501/v1/models/tomato_model")
            if res.status_code == 200:
                return {"status": "ok", "mode": "tf-serving"}
            return {"status": "fail", "details": res.json()}
        except Exception as e:
            return {"status": "fail", "error": str(e), "mode": "tf-serving"}
    else:
        if latest_model_file and os.path.exists(latest_model_file):
            return {"status": "ok", "mode": "local"}
        return {"status": "fail", "mode": "local", "error": "Model not found"}

@app.get("/model-info")
async def model_info():
    logging.info("Model info endpoint hit. Responding with model path and number of classes.")
    if not latest_model_file:
        return {"error": "No model loaded"}
    return {
        "model_path": str(latest_model_file),
        "num_classes": len(CLASS_NAMES),
        "use_tf_serving": USE_TF_SERVING
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile):
    start = time.time()
    try:
        image = read_file_as_image(await file.read())
        prediction = predict_model(image)
        logging.info(f"Prediction done in {round(time.time() - start, 4)}s: {prediction}")
        return PredictionResponse(**prediction)
    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)