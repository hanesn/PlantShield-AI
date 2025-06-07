import yaml
import os
from tensorflow.keras.callbacks import ReduceLROnPlateau,CSVLogger,ModelCheckpoint,EarlyStopping,TensorBoard

def load_params(path='../config/params.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def get_callbacks(
    early_stopping_patience,
    reduce_lr_factor,
    reduce_lr_patience,
    min_lr,
    logs_dir="../logs",
    checkpoints_dir="../checkpoints",
    csv_log_filename="training_log.csv",
    model_filename="best_model.keras",
):
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(checkpoints_dir, exist_ok=True)

    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=reduce_lr_factor,
        patience=reduce_lr_patience,
        verbose=1,
        min_lr=min_lr
    )

    csv_logger = CSVLogger(
        os.path.join(logs_dir, csv_log_filename),
        append=True
    )

    checkpoint = ModelCheckpoint(
        os.path.join(checkpoints_dir, model_filename),
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )

    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=early_stopping_patience,
        restore_best_weights=True,
        verbose=1
    )

    tensorboard = TensorBoard(
        log_dir=logs_dir
    )

    return [reduce_lr, csv_logger, checkpoint, early_stopping, tensorboard]