import threading
import time
from queue import Queue

import cv2

input_frames_queue = Queue(10)
out_put_frames_queue = Queue(10)


class ImageGrabber(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cam = cv2.VideoCapture(0)

    def run(self):
        global input_frames_queue
        while True:
            ret, frame = self.cam.read()
            input_frames_queue.put(frame)


class ImageDisplayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global out_put_frames_queue
        while True:
            if not out_put_frames_queue.empty():
                f = out_put_frames_queue.get()
                out_put_frames_queue.task_done()
                cv2.imshow('frame', f)
                key = cv2.waitKey(1) & 0xFF

class ImageProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global input_frames_queue
        global out_put_frames_queue
        while True:
            if not input_frames_queue.empty():
                f = input_frames_queue.get()
                input_frames_queue.task_done()
                out_put_frames_queue.put(f)


if __name__ == '__main__':
    grabber = ImageGrabber()
    displayer = ImageDisplayer()
    processer = ImageProcessor()
    grabber.start()
    displayer.start()
    processer.start()
