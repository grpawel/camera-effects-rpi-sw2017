import cv2
import threading

def observable_frames_cv2(observer):
    cap = cv2.VideoCapture(0)
    def loop():
        while True:
            ret, frame = cap.read()
            if not ret:
                observer.on_error("No camera feed")
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            print("frame")
            observer.on_next(cv2image)
    thread = threading.Thread(target=loop, args=[])
    thread.start()