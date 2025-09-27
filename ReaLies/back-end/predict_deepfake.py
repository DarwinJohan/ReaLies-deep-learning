#!/usr/bin/env python3
# predict_deepfake.py

import os
import sys
import math
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

# --- Config ---
MODEL_PATH = "CNN_RNN.h5"
VIDEO_PATH = "1.mp4"
IMAGE_SIZE = (224, 224)   # ResNet50 default
MAX_FRAMES = 20
THRESHOLD = 0.5

# --- Load pretrained CNN for feature extraction ---
cnn = ResNet50(weights="imagenet", include_top=False, pooling="avg")

# --- Load trained GRU model ---
if not os.path.exists(MODEL_PATH):
    print(f"[ERROR] Model file not found at {MODEL_PATH}")
    sys.exit(1)

model = load_model(MODEL_PATH, compile=False)
print("[OK] Model loaded:", MODEL_PATH)

# --- Helper: evenly sample frame indices ---
def get_sample_frame_indices(total_frames, num_samples):
    if total_frames <= 0:
        return []
    if total_frames <= num_samples:
        return list(range(total_frames))
    interval = total_frames / float(num_samples)
    return [min(total_frames - 1, math.floor(i * interval)) for i in range(num_samples)]

# --- Extract features from video ---
def extract_features(video_path, max_frames=MAX_FRAMES, image_size=IMAGE_SIZE):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    indices = get_sample_frame_indices(total_frames, max_frames)
    frames = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, image_size)
        frames.append(resized)

    cap.release()

    if len(frames) == 0:
        return None, None

    # preprocess
    arr = np.array(frames, dtype="float32")
    arr = preprocess_input(arr)  # ResNet preprocessing
    features = cnn.predict(arr, verbose=0)  # shape (N, 2048)

    # pad/truncate to max_frames
    if features.shape[0] < max_frames:
        pad_len = max_frames - features.shape[0]
        pad = np.zeros((pad_len, features.shape[1]))
        features = np.vstack([features, pad])
    elif features.shape[0] > max_frames:
        features = features[:max_frames]

    features = np.expand_dims(features, axis=0)  # (1, 20, 2048)

    # make mask (1 for real frames, 0 for padded)
    mask = np.ones((1, max_frames), dtype="float32")
    if features.shape[1] < max_frames:
        mask[:, features.shape[1]:] = 0

    return features, mask

# --- Prediction wrapper ---
def predict_video(video_path, model, threshold=THRESHOLD):
    feats, mask = extract_features(video_path)
    if feats is None:
        return {"status": "no_frames", "message": "No usable frames detected."}

    pred = model.predict([feats, mask], verbose=0)

    prob = float(pred[0, 1]) if pred.shape[-1] == 2 else float(pred[0, 0])
    label = "YES (FAKE)" if prob >= threshold else "NO (REAL)"

    return {"status": "ok", "probability": prob, "label": label}

# --- Main ---
if __name__ == "__main__":
    print("Model:", MODEL_PATH)
    print("Video:", VIDEO_PATH)
    res = predict_video(VIDEO_PATH, model, threshold=THRESHOLD)
    print(res)
