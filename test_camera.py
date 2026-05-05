import cv2

cap = cv2.VideoCapture(0)
print('Opened:', cap.isOpened())
if cap.isOpened():
    ret, frame = cap.read()
    print('Frame read:', ret)
    if ret:
        print('Shape:', frame.shape)
    cap.release()
else:
    print('Camera not opened')