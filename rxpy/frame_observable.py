import cv2
import threading

class CameraFeed():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def __iter__(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                observer.on_error("No camera feed")
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            yield cv2image
