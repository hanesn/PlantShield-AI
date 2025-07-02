from google.cloud import storage
from tensorflow.keras.models import load_model
from tensorflow import expand_dims
from PIL import Image
from flask import jsonify, make_response
import numpy as np

BUCKET_NAME = "tomato-disease-classification24"
MODEL_BLOB_PATH = "models/tomato_model-v1.keras"
MODEL_LOCAL_PATH = "/tmp/tomato_model-v1.keras"

CLASS_NAMES = [
    'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
    'Septoria_leaf_spot', 'Spider_mites_Two_spotted_spider_mite',
    'Target_Spot', 'YellowLeaf__Curl_Virus', 'mosaic_virus', 'healthy'
]

model = None

def download_model():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(MODEL_BLOB_PATH)
    blob.download_to_filename(MODEL_LOCAL_PATH)

def load_model_if_needed():
    global model
    if model is None:
        download_model()
        model = load_model(MODEL_LOCAL_PATH)

def predict(request):
    origin = request.headers.get("Origin")
    allowed_origins = ["http://localhost:3000","https://plantshieldai.netlify.app"]

    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": origin if origin in allowed_origins else "",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return ('', 204, headers)
    
    load_model_if_needed()

    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    try:
        file = request.files["file"]
        image = Image.open(file).convert("RGB").resize((256, 256))
        image_array = expand_dims(np.array(image), 0)

        predictions = model.predict(image_array, verbose=0)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]) * 100)

        headers = {
            "Access-Control-Allow-Origin": origin if origin in allowed_origins else "",
        }

        return make_response(
            jsonify({"class": predicted_class, "confidence": round(confidence, 2)}),
            200,
            headers
        )
    except Exception as e:
        headers = {
            "Access-Control-Allow-Origin": origin if origin in allowed_origins else "",
        }
        return make_response(jsonify({"error": str(e)}), 500, headers)