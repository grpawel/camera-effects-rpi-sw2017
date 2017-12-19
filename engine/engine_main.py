import threading
import time
from queue import Queue

import cv2


class ImageGrabber(threading.Thread):
    def __init__(self, input_frames_queue):
        threading.Thread.__init__(self)
        self.cam = cv2.VideoCapture(0)
        self.input_frames_queue = input_frames_queue

    def run(self):
        while True:
            ret, frame = self.cam.read()
            self.input_frames_queue.put(frame)


class ImageDisplayer(threading.Thread):
    def __init__(self, output_frames_queue):
        threading.Thread.__init__(self)
        self.output_frames_queue = output_frames_queue

    def run(self):
        while True:
            if not self.output_frames_queue.empty():
                f = self.output_frames_queue.get()
                self.output_frames_queue.task_done()
                cv2.imshow('frame', f)
                key = cv2.waitKey(1) & 0xFF


class ImageProcessor(threading.Thread):
    def __init__(self, input_frames_queue, output_frames_queue):
        threading.Thread.__init__(self)
        self.input_frames_queue = input_frames_queue
        self.output_frames_queue = output_frames_queue

    def run(self):
        while True:
            if not self.input_frames_queue.empty():
                f = self.input_frames_queue.get()
                self.input_frames_queue.task_done()
                self.output_frames_queue.put(f)


class ImagePipeline():
    def __init__(self):
        self.output_frames_queue = Queue(10)
        self.input_frames_queue = Queue(10)
        self.grabber = ImageGrabber(self.input_frames_queue)
        self.displayer = ImageDisplayer(self.output_frames_queue)
        self.processor = ImageProcessor(self.input_frames_queue, self.output_frames_queue)

    def run(self):
        self.grabber.start()
        self.displayer.start()
        self.processor.start()


def main():
    pipeline = ImagePipeline()
    pipeline.run()


if __name__ == '__main__':
    main()
