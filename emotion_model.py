"""Handles loading the Hugging Face Vision Transformer model and running emotion inference."""
import cv2
import numpy as np
from PIL import Image
from transformers import pipeline

MOODS = ["Happy 😄", "Sad 😢", "Angry 😠", "Surprised 😲", "Fearful 😨", "Neutral 😐"]

MODEL_ID = "trpakov/vit-face-expression"

# Each emotion maps to its own mood so the music mirrors how the user feels.
FER_TO_MOOD = {
    "happy": "Happy 😄",
    "sad": "Sad 😢",
    "angry": "Angry 😠",
    "disgust": "Angry 😠",
    "surprise": "Surprised 😲",
    "fear": "Fearful 😨",
    "neutral": "Neutral 😐",
}

print("Loading facial emotion recognition model...")
# TODO: Load the two model (face detection and emotion recognition)


def crop_face(image: Image.Image, margin: float = 0.25) -> tuple[Image.Image, bool]:
    """Crop to the largest detected face (plus some margin). Falls back to the full frame."""
    # TODO: Detect faces with OpenCV's Haar Cascade or DNN face detector, then crop to the largest one.

    return image.crop(box), True


def predict_emotion(image: Image.Image) -> dict:
    """Takes a PIL image, crops the face, runs inference, and maps the model's output to app moods."""
    # TODO: Crop the face and run the Hugging Face pipeline to get predictions.

    # Pipeline output is sorted by score: [{'label': 'happy', 'score': 0.92}, ...]
    # TODO: Map the top prediction to a mood and return a dict with the detected mood, raw label, confidence, and top 3 predictions.

    return {
        "detected": FER_TO_MOOD.get(top_pred["label"].lower(), "Neutral 😐"),
        "raw_label": top_pred["label"],
        "confidence": round(top_pred["score"], 2),
        "raw_predictions": predictions[:3],  # Top 3 for UI debugging
        "face_detected": face_found,
    }
