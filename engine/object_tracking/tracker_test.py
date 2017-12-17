from tracker import ObjectTracker
def track():
    import cv2
    import numpy as np
    red =(np.array([30, 150, 50]), np.array([255, 255, 255]))
    blue = (np.array([86, 31, 4]), np.array([220, 88, 50]))
    down,up = red
    ob_trcker = ObjectTracker(down, up)
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        frame = ob_trcker.process(img)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
if __name__ == '__main__':
    track()