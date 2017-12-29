
from threading import Thread
import cv2

from engine.face_filters.face_detector import face_detector


class WebcamVideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):

        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

vs = WebcamVideoStream(src=0).start()

while True:



    frame = vs.read()
    im = face_detector(frame, faces=True, mouths=True)
    cv2.imshow("Frame", im)
    key = cv2.waitKey(1) & 0xFF
