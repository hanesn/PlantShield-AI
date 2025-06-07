import numpy as np
from training.utils import inference_utils
import matplotlib
matplotlib.use("Agg")

class DummyModel:
    def predict(self, batch, verbose=0):
        return np.array([[0.1, 0.3, 0.05, 0.4, 0.15]])

def test_predict_top_k():
    model = DummyModel()
    image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    class_names = ['A', 'B', 'C', 'D', 'E']
    
    preds = inference_utils.predict_top_k(model, image, class_names, k=3)
    
    assert isinstance(preds, list)
    assert len(preds) == 3
    assert all(isinstance(p, tuple) for p in preds)

def test_plot_image_with_topk_predictions():
    image = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    topk_preds = [('A', 0.6), ('B', 0.3), ('C', 0.1)]

    inference_utils.plot_image_with_topk_predictions(image, topk_preds, title="Test Image")
