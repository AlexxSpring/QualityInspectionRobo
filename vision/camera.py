import cv2
import time

from vision.processor import extract_object
from vision.classifier import classify_object

camera = None  # global camera object
use_picamera = False

def generate_frames():
    global camera, use_picamera

    # =========================
    # Initialize camera
    # =========================
    if camera is None:
        # Try OpenCV first (for USB cameras)
        for i in range(3):  # try multiple indexes
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                camera = cam
                use_picamera = False
                print(f"✅ OpenCV camera opened on index {i}")
                break

        # If OpenCV failed, try PiCamera
        if camera is None or not camera.isOpened():
            try:
                from picamera import PiCamera
                from picamera.array import PiRGBArray
                camera = PiCamera()
                camera.resolution = (640, 480)
                camera.framerate = 30
                raw_capture = PiRGBArray(camera, size=(640, 480))
                time.sleep(0.1)  # warm up
                use_picamera = True
                print("✅ PiCamera opened")
            except ImportError:
                print("❌ PiCamera not available")
            except Exception as e:
                print(f"❌ PiCamera error: {e}")

    if camera is None:
        print("❌ No camera available")
        return

    # =========================
    # Main Loop
    # =========================
    if use_picamera:
        # PiCamera streaming
        from picamera.array import PiRGBArray
        raw_capture = PiRGBArray(camera, size=(640, 480))
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            image = frame.array

            # Process frame
            process_and_yield_frame(image)

            raw_capture.truncate(0)
            time.sleep(0.03)
    else:
        # OpenCV loop
        while True:
            success, frame = camera.read()

            # Safety check
            if not success or frame is None:
                print("⚠ Frame read failed, skipping")
                time.sleep(0.1)  # wait a bit before retry
                continue

            process_and_yield_frame(frame)

def process_and_yield_frame(frame):
    # ========================= 
    h, w, _ = frame.shape

    roi_x1 = int(w * 0.3)
    roi_y1 = int(h * 0.4)
    roi_x2 = int(w * 0.7)
    roi_y2 = int(h * 0.8)

    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]

    # Draw ROI box (BLUE)
    cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 255, 0), 2)

    # =========================
    # STEP 1: Detect object
    # =========================
    cropped, box = extract_object(roi)

    if box is not None and cropped is not None:
        x, y, bw, bh = box
        x+= roi_x1
        y+= roi_y1

        # =========================
        # STEP 2: Dimension
        # =========================
        pixel_to_cm = 0.02  # 🔧 calibrate later
        width_cm = bw * pixel_to_cm
        height_cm = bh * pixel_to_cm

        # =========================
        # STEP 3: Classification
        # =========================
        label, conf = classify_object(cropped)

        # =========================
        # Draw bounding box
        # =========================
        color = (0, 255, 0) if "Good" in label else (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x + bw, y + bh), color, 2)

        # Label background
        cv2.rectangle(frame, (x, y - 30), (x + bw, y), (0, 0, 0), -1)

        # Label text
        cv2.putText(
            frame,
            f"{label} ({conf:.2f})",
            (x + 5, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        # Dimension text
        cv2.putText(
            frame,
            f"W:{width_cm:.2f}cm H:{height_cm:.2f}cm",
            (x, y + bh + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            2
        )

    # =========================
    # Convert frame to JPEG
    # =========================
    ret, buffer = cv2.imencode('.jpg', frame)

    if not ret:
        return

    frame_bytes = buffer.tobytes()

    # =========================
    # Stream frame (FASTAPI)
    # =========================
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' +
           frame_bytes + b'\r\n')

    time.sleep(0.03)
