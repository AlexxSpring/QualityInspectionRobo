import cv2
import numpy as np

# Simplified classifier without TFLite dependency
MODEL_LOADED = False

# =========================
# LABELS (EDIT IF NEEDED)
# =========================
labels = [
    "Screw_Good",
    "Screw_Defective",
    "Ball_Good",
    "Ball_Defective"
]


# =========================
# CLASSIFICATION FUNCTION
# =========================
def classify_object(image):
    """
    Input: cropped image (numpy array)
    Output: label, confidence
    """

    # Always return fallback since no model
    return "No_Model", 0.0
