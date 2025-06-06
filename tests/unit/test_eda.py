import tensorflow as tf
from training.utils import eda
import matplotlib
matplotlib.use("Agg")

class_names = ['A', 'B', 'C']

def get_dummy_dataset(num_samples=16):
    images = tf.random.uniform((num_samples, 128, 128, 3))
    labels = tf.constant([i % 3 for i in range(num_samples)])  # rotate 0/1/2
    return tf.data.Dataset.from_tensor_slices((images, labels)).batch(num_samples)

def dummy_augment_fn(images):
    return images + tf.random.uniform(tf.shape(images), 0, 0.1)

def test_plot_sample_images():
    ds = get_dummy_dataset(16)
    eda.plot_sample_images(ds, class_names)

def test_plot_augmented_images():
    ds = get_dummy_dataset(8)
    eda.plot_augmented_images(ds, dummy_augment_fn, class_names, num_images=8)
