import matplotlib.pyplot as plt

def plot_sample_images(dataset, class_names, rows=4, cols=4):
    plt.figure(figsize=(10, 10))
    images, labels = next(iter(dataset))  # grab one batch

    for i in range(16):
        ax = plt.subplot(4, 4, i + 1)
        # images are [0–255], so divide by 255 and set vmin/vmax
        ax.imshow(images[i].numpy() / 255.0, vmin=0, vmax=1)
        ax.set_title(class_names[labels[i].numpy()])
        ax.axis("off")

    plt.tight_layout()
    plt.show()

def plot_augmented_images(dataset, augment_fn, class_names, num_images=8):
    images, labels = next(iter(dataset))  # get one batch
    augmented_images = augment_fn(images)

    plt.figure(figsize=(2 * num_images, 5))

    for i in range(num_images):
        # Top row: Original
        ax = plt.subplot(2, num_images, i + 1)
        ax.imshow(images[i].numpy() / 255.0, vmin=0, vmax=1)
        ax.set_title(class_names[labels[i].numpy()], fontsize=10)
        ax.axis("off")

        # Bottom row: Augmented
        ax = plt.subplot(2, num_images, i + 1 + num_images)
        ax.imshow(augmented_images[i].numpy() / 255.0, vmin=0, vmax=1)
        ax.set_title("Augmented", fontsize=10)
        ax.axis("off")

    plt.tight_layout()
    plt.show()