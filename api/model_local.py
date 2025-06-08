from tensorflow.keras.models import load_model
from pathlib import Path
import numpy as np
from utils import CLASS_NAMES

saved_model_dir = Path('saved_models')
model_files = sorted(saved_model_dir.glob("tomato_model-v*.keras"))
latest_model_file = max(model_files, key=lambda p: int(p.stem.split("-v")[-1]))
model = load_model(latest_model_file)

def predict_local(image: np.ndarray) -> dict:
    image_batch = np.expand_dims(image, 0)
    prediction = model.predict(image_batch, verbose=0)
    class_id = int(np.argmax(prediction, axis=1)[0])
    predicted_class=CLASS_NAMES[class_id]
    confidence = float(np.max(prediction))
    return {
        "Class": predicted_class,
        "Confidence": confidence
    }
