import cv2
import numpy as np

# TensorFlow Lite import
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    try:
        import tensorflow.lite as tflite
    except ImportError:
        tflite = None

# =========================
# LOAD MODEL (runs once)
# =========================
interpreter = None
input_details = None
output_details = None

if tflite:
    try:
        # 👉 Make sure this path is correct
        interpreter = tflite.Interpreter(model_path="models/prediction.tflite")
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        MODEL_LOADED = True
        print("✅ TFLite model loaded successfully")

    except Exception as e:
        print("❌ Model load failed:", e)
        MODEL_LOADED = False
else:
    print("❌ TFLite not available")
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
        interpreter.set_tensor(input_details[0]['index'], img)
        interpreter.invoke()
        preds = interpreter.get_tensor(output_details[0]['index'])[0]

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
