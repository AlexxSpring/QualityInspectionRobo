import cv2
import numpy as np

def extract_object(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🔥 Smooth
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # 🔥 Adaptive threshold (handles lighting)
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # 🔥 Remove noise / join parts
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, None

    # ❗ ignore tiny junk
    contours = [c for c in contours if cv2.contourArea(c) > 500]
    if not contours:
        return None, None

    # pick biggest valid object
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)

    cropped = frame[y:y+h, x:x+w]

    return cropped, (x, y, w, h)
