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
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

    def run(self):
        global input_frames_queue
        global out_put_frames_queue
        while True:
            if not input_frames_queue.empty():
                f = input_frames_queue.get()
                processed = self.target.process(f)
                input_frames_queue.task_done()
                out_put_frames_queue.put(processed)

class BaseTarget(object):
    def process(self, img):
        raise NotImplementedError("Please Implement this method")

if __name__ == '__main__':
    import numpy as np
    from engine.object_tracking.tracker import ObjectTracker

    down,up = (np.array([30, 150, 50]), np.array([255, 255, 255]))
    target = ObjectTracker(down,up)
    grabber = ImageGrabber()
    displayer = ImageDisplayer()
    processer = ImageProcessor(target)
    grabber.start()
    displayer.start()
    processer.start()
