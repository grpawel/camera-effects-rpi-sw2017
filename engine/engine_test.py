
from threading import Thread
import cv2

from engine.face_filters.face_detector import FaceDetector

vs = cv2.VideoCapture(0)

fd = FaceDetector(True, True, False, True, True)



while True:



    _,frame = vs.read()
    im = fd.procces_img(frame)
    cv2.imshow("Frame", im)
    key = cv2.waitKey(1) & 0xFF
