from engine.object_tracking.tracker import ObjectTracker


def track():
    import cv2
    import numpy as np
    red = (np.array([30, 150, 50]), np.array([255, 255, 255]))
    blue = (np.array([46, 31, 240]), np.array([255, 255, 255]))
    green = (np.array([106, 11, 240]), np.array([255, 255, 255]))
    down, up = red
    ob_trcker = ObjectTracker(down, up)
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        name, frame = ob_trcker.process(img)
        cv2.imshow(name, frame)
        key = cv2.waitKey(1) & 0xFF


if __name__ == '__main__':
    track()
