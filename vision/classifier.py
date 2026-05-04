import cv2
import numpy as np

# OpenVINO import
from openvino import Core

# =========================
# LOAD MODEL (runs once)
# =========================
try:
    ie = Core()

    # 👉 Make sure this path is correct
    model = ie.read_model("models/prediction.tflite")

    compiled_model = ie.compile_model(model, "CPU")

    input_layer = compiled_model.input(0)
    output_layer = compiled_model.output(0)

    MODEL_LOADED = True
    print("✅ OpenVINO model loaded successfully")

except Exception as e:
    print("❌ Model load failed:", e)
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

    # 🔴 If model not loaded → fallback
    if not MODEL_LOADED:
        return "Model_Not_Loaded", 0.0

    try:
        # =========================
        # PREPROCESS
        # =========================
        img = cv2.resize(image, (224, 224))   # ⚠ adjust if needed
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        # =========================
        # INFERENCE
        # =========================
        result = compiled_model([img])[output_layer]
        preds = result[0]

        # =========================
        # POSTPROCESS
        # =========================
        idx = int(np.argmax(preds))
        conf = float(np.max(preds))

        label = labels[idx] if idx < len(labels) else "Unknown"

        return label, conf

    except Exception as e:
        print("⚠ Inference error:", e)
        return "Error", 0.0
