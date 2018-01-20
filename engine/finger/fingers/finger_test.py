import cv2
from engine.finger.fingers.finger_processor import finger_processor

cap = cv2.VideoCapture(0)

if __name__ == '__main__':

    while True:
        _, img = cap.read()
        name, frame = finger_processor(img)
        cv2.imshow(name, frame)
        key = cv2.waitKey(1) & 0xFF