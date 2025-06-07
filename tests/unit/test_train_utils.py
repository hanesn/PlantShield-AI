import tensorflow as tf
import tempfile
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import training.utils.train_utils as tu

# Dummy class names
class_names = ['A', 'B', 'C']
IMAGE_SIZE = 256
BATCH_SIZE = 12
CHANNELS = 3

def get_dummy_dataset(num_samples=12):
    images = tf.random.uniform((num_samples, IMAGE_SIZE, IMAGE_SIZE, CHANNELS))
    labels = tf.random.uniform((num_samples,), maxval=len(class_names), dtype=tf.int32)
    ds = tf.data.Dataset.from_tensor_slices((images, labels))
    ds = ds.batch(BATCH_SIZE)
    return ds

def test_build_and_compile_model():
    model = tu.build_model(IMAGE_SIZE, class_names, BATCH_SIZE, CHANNELS)
    assert model.input_shape == (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS)
    tu.compile_model(model, learning_rate=0.001)
    assert model.loss.__class__.__name__ == 'SparseCategoricalCrossentropy'

def test_train_model():
    model = tu.build_model(IMAGE_SIZE, class_names, BATCH_SIZE, CHANNELS)
    tu.compile_model(model, learning_rate=0.001)
    train_ds = get_dummy_dataset()
    val_ds = get_dummy_dataset()
    history = tu.train_model(model, epochs=1, train_ds=train_ds, val_ds=val_ds, callbacks=[], class_weights=None)
    print(history.history)
    assert 'accuracy' in history.history
    assert 'loss' in history.history
    assert 'val_accuracy' in history.history
    assert 'val_loss' in history.history

def test_predict_image():
    model = tu.build_model(IMAGE_SIZE, class_names, BATCH_SIZE, CHANNELS)
    tu.compile_model(model, learning_rate=0.001)
    # Create dummy image
    images = tf.random.uniform((BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, CHANNELS))
    for i in range(BATCH_SIZE):
        img = images[i]  # single image tensor (IMAGE_SIZE, IMAGE_SIZE, CHANNELS)
        
        # Call predict_image on each single image
        predicted_class, confidence = tu.predict_image(model, img, class_names)
        
        # Assertions for each image prediction
        assert predicted_class in class_names
        assert 0 <= confidence <= 100

def test_plot_metrics_creates_files_and_plots():
    # Create a temp CSV file with dummy history data
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, 'history.csv')
        data = {
            'accuracy': [0.1, 0.2, 0.3],
            'val_accuracy': [0.1, 0.15, 0.25],
            'loss': [2.0, 1.5, 1.0],
            'val_loss': [2.1, 1.6, 1.1],
            'learning_rate': [0.001, 0.0005, 0.0001]
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)

        save_dir = os.path.join(tmpdir, 'plots')
        tu.plot_metrics(csv_path, save_dir)

        # Check if files are created
        assert os.path.exists(os.path.join(save_dir, 'accuracy_loss.png'))
        assert os.path.exists(os.path.join(save_dir, 'learning_rate.png'))
        assert os.path.exists(os.path.join(save_dir, 'val_loss_vs_lr.png'))
