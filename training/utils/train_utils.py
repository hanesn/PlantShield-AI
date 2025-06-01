import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras import layers,models
import os
import numpy as np
import pandas as pd
import seaborn as sns

def build_model(image_size,class_names,batch_size,channels):
    resize_and_rescale=tf.keras.Sequential([
        layers.Resizing(image_size,image_size),
        layers.Rescaling(1.0/255)
    ])

    augment=tf.keras.Sequential([
        layers.RandomFlip(),
        layers.RandomRotation(.2)
    ])
    model=models.Sequential([
        resize_and_rescale,
        augment,
        layers.Conv2D(32,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Conv2D(64,(3,3),activation='relu'),
        layers.MaxPool2D((2,2)),
        layers.Flatten(),
        layers.Dense(64,activation='relu'),
        layers.Dense(len(class_names),activation='softmax')
    ])
    model.build(input_shape=(batch_size,image_size,image_size,channels))
    return model

def compile_model(model,learning_rate):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )

def train_model(model,epochs, train_ds, val_ds, callbacks, class_weights):
    history=model.fit(
        train_ds,
        epochs=epochs,
        validation_data=val_ds,
        callbacks=callbacks,
        class_weight=class_weights
    )
    return history

def predict_image(model, img, class_names):
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array, verbose=0)
    predicted_class = class_names[tf.math.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence

def plot_metrics(csv_path, save_dir):
    # Read CSV
    history_df = pd.read_csv(csv_path)

    # Set Seaborn style
    plt.figure(figsize=(14, 6))

    # Plot 1: Accuracy
    plt.subplot(1, 2, 1)
    sns.lineplot(x=range(len(history_df)), y=history_df['accuracy'], label='Train Accuracy', linewidth=2, color="#1f77b4")
    sns.lineplot(x=range(len(history_df)), y=history_df['val_accuracy'], label='Val Accuracy', linewidth=2, color="#ff7f0e")
    plt.fill_between(range(len(history_df)), history_df['accuracy'], history_df['val_accuracy'], alpha=0.1, color="#1f77b4")
    plt.title("Training vs Validation Accuracy", fontsize=14, weight='bold')
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    # Plot 2: Loss
    plt.subplot(1, 2, 2)
    sns.lineplot(x=range(len(history_df)), y=history_df['loss'], label='Train Loss', linewidth=2, color="#d62728")
    sns.lineplot(x=range(len(history_df)), y=history_df['val_loss'], label='Val Loss', linewidth=2, color="#2ca02c")
    plt.fill_between(range(len(history_df)), history_df['loss'], history_df['val_loss'], alpha=0.1, color="#d62728")
    plt.title("Training vs Validation Loss", fontsize=14, weight='bold')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    # Layout + Save
    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, "accuracy_loss.png"), dpi=300)
    plt.show()