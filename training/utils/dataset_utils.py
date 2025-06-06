import os
from collections import Counter
import json
from tensorflow.data import AUTOTUNE

def get_dataset_partitions_tf(dataset,train_split=.8,val_split=.1,test_split=.1,shuffle=True):
    train_size = int(len(dataset) * train_split)
    val_size = int(len(dataset) * val_split)
    test_size = len(dataset) - train_size - val_size
    train_ds=dataset.take(train_size)
    val_ds=dataset.skip(train_size).take(val_size)
    test_ds=dataset.skip(train_size+val_size)
    print("Full dataset length = ",len(dataset))
    print("train dataset length = ",len(train_ds))
    print("validation dataset length = ",len(val_ds))
    print("test dataset length = ",len(test_ds))
    return train_ds,val_ds,test_ds

def get_or_compute_class_weights(dataset, class_weights_path='../config/class_weights.json'):
    if os.path.exists(class_weights_path):
        print(f"Found existing class weights at {class_weights_path}. Loading...")
        with open(class_weights_path, 'r') as f:
            class_weights = json.load(f)
        # Keys come as strings in JSON, convert back to int
        class_weights = {int(k): v for k, v in class_weights.items()}
    else:
        print("Class weights not found. Computing from dataset...")
        all_labels = []
        for images, labels in dataset:
            all_labels.extend([int(label) for label in labels.numpy()])

        label_counts = Counter(all_labels)
        total_samples = sum(label_counts.values())
        class_weights = {
            label: total_samples / (len(label_counts) * count)
            for label, count in label_counts.items()
        }

        os.makedirs(os.path.dirname(class_weights_path), exist_ok=True)
        with open(class_weights_path, 'w') as f:
            json.dump(class_weights, f, indent=4)
        print(f"Class weights saved to {class_weights_path}")
    
    return class_weights

def preprocess_dataset(ds, shuffle_buffer=1000):
    return ds.cache().shuffle(shuffle_buffer).prefetch(AUTOTUNE)
