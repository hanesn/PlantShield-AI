# GCP Cloud Function Deployment for Tomato Disease Classification

This guide outlines how to deploy the `predict` function using Google Cloud Functions, designed to classify tomato leaf diseases using a Keras model stored in a GCS bucket.

## Prerequisites

- A trained `.keras` model file.
- Google Cloud CLI (`gcloud`) installed and initialized.
- A Google Cloud project set up.

## Steps to Deploy

### 1. Create a GCP Project

- Go to: https://console.cloud.google.com/
- Click on the project dropdown and create a new project (e.g., `tomato-disease-classification`).

### 2. Enable Required APIs

- From Cloud Console:
Go to `APIs & Services > Library` and enable:

  - Cloud Functions API
  - Cloud Storage API

### 3. Create a Cloud Storage Bucket

- Go to `Storage > Buckets`
- Click Create bucket:
    - Name: tomato-classification-bucket-tflite
    - Location: us-central1 (or your preferred region)

### 4. Upload the Model

- Inside the bucket, create a folder called `models/`
- Upload your model as:
`models/tomatoes_model-v1.keras`

### 5. Prepare Local Code

Your `main.py` should include:

```
MODEL_LOCAL_PATH = "/tmp/tomatoes_model-v1.keras"
```

Why `/tmp/`?

- Cloud Functions have a read-only filesystem.
- The only writable directory is `/tmp/`, so any downloaded files (like the model) must be stored there.

### 6. Initialize gcloud

Open terminal:

```bash
gcloud init
```

### 7. Deploy the Function

Navigate to your `gcp/` directory:

```bash
cd gcp/
```

Then deploy:
```bash
gcloud functions deploy predict \
  --runtime python310 \
  --trigger-http \
  --memory=1024
```

### Testing

Once deployed, get the URL from the terminal and test using Postman or cURL:
- Method: `POST`
- URL: `https://<region>-<project>.cloudfunctions.net/predict`
- Body: form-data
    - Key: file
    - Type: File
- Upload an image file