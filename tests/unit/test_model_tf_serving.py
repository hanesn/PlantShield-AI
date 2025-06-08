import numpy as np
import pytest
from api.model_tf_serving import predict_tf_serving

@pytest.mark.skip(reason="Requires live TF Serving running on localhost:8501")
def test_predict_tf_serving():
    dummy_image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    result = predict_tf_serving(dummy_image)

    assert isinstance(result, dict)
    assert "Class" in result
    assert "Confidence" in result
    assert isinstance(result["Class"], str)
    assert isinstance(result["Confidence"], float)
