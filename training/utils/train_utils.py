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
    epochs = range(len(history_df))
    os.makedirs(save_dir, exist_ok=True)

    # Set Seaborn style
    sns.set_style("whitegrid")
    plt.figure(figsize=(14, 5))

    # Plot 1: Accuracy
    plt.subplot(1, 2, 1)
    sns.lineplot(x=epochs, y=history_df['accuracy'], label='Train Accuracy', linewidth=2, color="#1f77b4")
    sns.lineplot(x=epochs, y=history_df['val_accuracy'], label='Val Accuracy', linewidth=2, color="#ff7f0e")
    plt.fill_between(epochs, history_df['accuracy'], history_df['val_accuracy'], alpha=0.1, color="#1f77b4")
    plt.title("Training vs Validation Accuracy", fontsize=14, weight='bold')
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)

    # Plot 2: Loss
    plt.subplot(1, 2, 2)
    sns.lineplot(x=epochs, y=history_df['loss'], label='Train Loss', linewidth=2, color="#d62728")
    sns.lineplot(x=epochs, y=history_df['val_loss'], label='Val Loss', linewidth=2, color="#2ca02c")
    plt.fill_between(epochs, history_df['loss'], history_df['val_loss'], alpha=0.1, color="#d62728")
    plt.title("Training vs Validation Loss", fontsize=14, weight='bold')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "accuracy_loss.png"), dpi=300)
    plt.show()

    if 'learning_rate' in history_df.columns:
        plt.figure(figsize=(14, 5))
        sns.lineplot(x=epochs, y=history_df['learning_rate'], marker='o', color='teal', label="Learning rate")
        plt.title("Learning Rate Schedule", fontsize=14, weight='bold')
        plt.xlabel("Epoch")
        plt.ylabel("Learning Rate")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, "learning_rate.png"), dpi=300)
        plt.show()

        # Learning Rate vs Validation Loss
        fig, ax1 = plt.subplots(figsize=(14, 5))
        ax1.set_xlabel('Epoch')

        # Val Loss with fill
        val_loss = history_df['val_loss']
        ax1.plot(epochs, val_loss, color='crimson', label='Val Loss', marker='o', linewidth=2)
        ax1.fill_between(epochs, val_loss, alpha=0.3, color='crimson')  # fill area under curve
        ax1.set_ylabel('Val Loss', color='crimson')
        ax1.tick_params(axis='y', labelcolor='crimson')

        # Learning Rate on twin axis
        ax2 = ax1.twinx()
        learning_rate = history_df['learning_rate']
        ax2.plot(epochs, learning_rate, color='navy', label='Learning Rate', linestyle='--', linewidth=2)
        ax2.set_ylabel('Learning Rate', color='navy')
        ax2.tick_params(axis='y', labelcolor='navy')

        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        plt.title("Validation Loss vs Learning Rate", fontsize=14, weight='bold')
        fig.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.savefig(os.path.join(save_dir, "val_loss_vs_lr.png"), dpi=300)
        plt.show()