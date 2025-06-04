from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

CLASS_NAMES=['Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold', 'Septoria_leaf_spot', 'Spider_mites_Two_spotted_spider_mite', 'Target_Spot', 'YellowLeaf__Curl_Virus', 'mosaic_virus', 'healthy']

def load_image(image_path):
    img = Image.open(image_path).convert("RGB")  # ensure 3 channels
    return np.array(img)

def predict_top_k(model, image, class_names, k=3):
    img_batch = np.expand_dims(image, axis=0)
    predictions = model.predict(img_batch,verbose=0)[0]
    top_k_indices = np.argsort(predictions)[::-1][:k]
    return [(class_names[i], predictions[i]) for i in top_k_indices]

def plot_image_with_topk_predictions(image, topk_preds, title=None):
    """
    image: numpy array (H, W, 3)
    topk_preds: list of tuples (class_name, confidence)
    """
    fig, (ax_img, ax_bar) = plt.subplots(1, 2, figsize=(10, 3), gridspec_kw={'width_ratios': [2, 3]})
    
    # Image
    ax_img.imshow(image)
    ax_img.axis('off')
    if title:
        ax_img.set_title(title, fontsize=10)

    # Bar Plot
    class_names = [cls for cls, _ in topk_preds]
    confidences = [conf for _, conf in topk_preds]

    y_pos = np.arange(len(class_names))
    ax_bar.barh(y_pos, confidences, color='skyblue')
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(class_names)
    ax_bar.invert_yaxis()  # Highest on top
    ax_bar.set_xlabel("Confidence")
    ax_bar.set_xlim(0, 1)

    plt.tight_layout()
    plt.show()