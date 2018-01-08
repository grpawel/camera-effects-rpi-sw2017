from engine.object_tracking.tracker import ObjectTracker
import cv2
import numpy as np
def rgb_to_hsv(rgb):
    r,g,b = rgb
    return cv2.cvtColor(np.uint8([[[r,g,b]]]), cv2.COLOR_RGB2HSV)

def track():
    import cv2
    import numpy as np
    red =(np.array([30, 150, 50]), np.array([255, 255, 255]))
    blue = (np.array([110,50,50]), np.array([130,255,255]))
    green = (np.array([28,102,81]), np.array([100,255,150]))
    green = (np.array([28,102,81]), np.array([100,255,150]))


    down,up = green
    ob_trcker = ObjectTracker((40,50,50), (80,255,255))
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        frame = ob_trcker.track(img)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
if __name__ == '__main__':
    track()
