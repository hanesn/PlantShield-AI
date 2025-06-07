from training.utils import config
import os

def test_load_params():
    path = os.path.join("training", "config", "params.yaml")
    params = config.load_params(path)

    # Check that required fields exist
    assert isinstance(params, dict)
    
    # Important fixed config values that can break things if changed
    assert "image_size" in params
    assert "channels" in params
    assert params["image_size"] == 256
    assert params["channels"] == 3

    # validate types
    assert isinstance(params["image_size"], int)
    assert isinstance(params["channels"], int)

def test_get_callbacks(tmp_path):
    callbacks = config.get_callbacks(
        early_stopping_patience=3,
        reduce_lr_factor=0.1,
        reduce_lr_patience=2,
        min_lr=1e-5,
        logs_dir=tmp_path / "logs",
        checkpoints_dir=tmp_path / "checkpoints"
    )
    assert len(callbacks) == 5
