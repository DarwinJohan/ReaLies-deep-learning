import os
import random
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras import layers, models

random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

IMAGE_SIZE = (256, 256)
THRESHOLD = 0.5

_mesonet_model = None

class MesoNet:
    def __init__(self):
        self.model = self.build_model()
        self.model_size = IMAGE_SIZE
        
    def build_model(self):
        """Build MesoNet architecture"""
        model = models.Sequential([
            layers.Conv2D(8, (3, 3), padding='same', activation='relu', input_shape=(256, 256, 3)),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size=(2, 2)),
            
            layers.Conv2D(8, (5, 5), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size=(2, 2)),

            layers.Conv2D(16, (5, 5), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size=(2, 2)),

            layers.Conv2D(16, (5, 5), padding='same', activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size=(4, 4)),
            
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(16, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def predict_video(self, video_path, num_frames=20):
        """Predict using MesoNet"""
        frames = self.extract_frames(video_path, num_frames)
        if not frames:
            return {"error": "No frames extracted"}
        
        predictions = []
        for frame in frames:
            try:
                frame_resized = cv2.resize(frame, self.model_size)
                frame_normalized = frame_resized.astype('float32') / 255.0
                frame_expanded = np.expand_dims(frame_normalized, axis=0)
                
                pred = self.model.predict(frame_expanded, verbose=0)[0][0]
                predictions.append(pred)
            except Exception as e:
                print(f"⚠️  MesoNet frame error: {e}")
                continue
        
        if not predictions:
            return {"error": "All frame predictions failed"}
        
        avg_pred = np.mean(predictions)
        median_pred = np.median(predictions)
        std_pred = np.std(predictions)
        
        return {
            "probability_fake": float(avg_pred),
            "probability_real": float(1 - avg_pred),
            "median_probability": float(median_pred),
            "std_deviation": float(std_pred),
            "frames_analyzed": len(predictions),
            "model": "MesoNet",
            "consistency": "HIGH" if std_pred < 0.15 else "MEDIUM" if std_pred < 0.25 else "LOW"
        }
    
    def extract_frames(self, video_path, num_frames=20):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ Cannot open video: {video_path}")
            return []
        
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            print("❌ Video has 0 frames")
            cap.release()
            return []
        
        if total_frames <= num_frames:
            frame_indices = range(total_frames)
        else:
            frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
            frame_indices = [min(max(0, idx + random.randint(-2, 2)), total_frames-1) 
                           for idx in frame_indices]
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret and frame is not None:
                frames.append(frame)
        
        cap.release()
        print(f"📹 Extracted {len(frames)} frames from {total_frames} total frames")
        return frames

def load_mesonet():
    global _mesonet_model
    if _mesonet_model is None:
        _mesonet_model = MesoNet()
        print("✅ MesoNet loaded")
    return _mesonet_model

def predict_video(video_path, threshold=THRESHOLD):
    print("=" * 70)
    print("🤖 DEEPFAKE DETECTION (MesoNet)")
    print(f"🎬 Video: {os.path.basename(video_path)}")
    print("=" * 70)
    
    if not os.path.exists(video_path):
        return {
            "status": "error",
            "message": f"Video file not found: {video_path}",
            "label": "ERROR",
            "confidence": "LOW"
        }
    
    model = load_mesonet()
    result = model.predict_video(video_path)
    
    if "error" in result:
        return {
            "status": "error",
            "message": result["error"],
            "label": "UNCERTAIN",
            "confidence": "LOW"
        }
    
    prob_fake = result["probability_fake"]
    
    if prob_fake > threshold + 0.2:
        label = "YES (FAKE)"
    elif prob_fake > threshold + 0.1:
        label = "LIKELY FAKE"
    elif prob_fake > threshold:
        label = "POSSIBLY FAKE"
    elif prob_fake < threshold - 0.2:
        label = "NO (REAL)"
    elif prob_fake < threshold - 0.1:
        label = "LIKELY REAL"
    else:
        label = "UNCERTAIN"
    
    final_result = {
        "status": "ok",
        "label": label,
        "probability_fake": prob_fake,
        "probability_real": 1 - prob_fake,
        "frames_analyzed": result["frames_analyzed"],
        "consistency": result["consistency"],
        "model": "MesoNet",
        "confidence": "HIGH" if result["consistency"] == "HIGH" else "MEDIUM" if result["consistency"] == "MEDIUM" else "LOW"
    }

    
    print(f"   ✅ Fake Probability: {prob_fake:.4f}")
    print(f"   🎯 Final Decision: {label}")
    print("=" * 70)
    return final_result

if __name__ == "__main__":
    import sys
    video_path = sys.argv[1] if len(sys.argv) > 1 else "1.mp4"
    result = predict_video(video_path)
    print(result)
