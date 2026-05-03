import asyncio
import logging

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    logging.warning("OpenCV not available. Falling back to mock camera.")
    OPENCV_AVAILABLE = False

async def generate_frames():
    """
    OpenCV camera frame generator with mock fallback.
    Yields motion jpeg stream.
    """
    if OPENCV_AVAILABLE:
        # Try to open the default camera
        cap = cv2.VideoCapture(0)
        
        # If camera opened successfully
        if cap.isOpened():
            try:
                while True:
                    success, frame = cap.read()
                    if not success:
                        break
                    
                    # Add a simple text overlay
                    cv2.putText(frame, "IotRoboDash LIVE", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    await asyncio.sleep(0.05) # ~20 fps
            finally:
                cap.release()
                
    # Fallback if no OpenCV or no camera found
    while True:
        dummy_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\x00\xff\xd9'
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + dummy_jpeg + b'\r\n')
        await asyncio.sleep(0.1)
