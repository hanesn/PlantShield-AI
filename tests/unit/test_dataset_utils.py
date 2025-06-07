import tensorflow as tf
import os
from training.utils import dataset_utils
import tempfile

def test_get_dataset_partitions_tf():
    data = tf.data.Dataset.range(10).map(lambda x: (x, x % 2))
    train, val, test = dataset_utils.get_dataset_partitions_tf(data, 0.8, 0.1, 0.1)
    assert len(list(train)) == 8
    assert len(list(val)) == 1
    assert len(list(test)) == 1

def test_preprocess_dataset():
    data = tf.data.Dataset.range(5).map(lambda x: (x, x))
    preprocessed = dataset_utils.preprocess_dataset(data)
    assert isinstance(preprocessed, tf.data.Dataset)

def test_get_or_compute_class_weights():
    # Simulate a batched dataset like the real one
    images = tf.random.uniform((12, 256, 256, 3))  # batch of 12 images
    labels = tf.constant([0, 1, 0, 3, 2, 4, 5, 6, 7, 8, 9, 4])  # batch of 12 labels
    dataset = tf.data.Dataset.from_tensor_slices((images, labels)).batch(4)  # simulate batching

    with tempfile.TemporaryDirectory() as tmpdir:
        class_weights_path = os.path.join(tmpdir, "class_weights.json")

        class_weights = dataset_utils.get_or_compute_class_weights(dataset, class_weights_path)

        assert isinstance(class_weights, dict)
        assert all(isinstance(k, int) for k in class_weights.keys())
        assert all(isinstance(v, float) for v in class_weights.values())

        class_weights_loaded = dataset_utils.get_or_compute_class_weights(dataset, class_weights_path)
        assert class_weights == class_weights_loaded
