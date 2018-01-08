import cv2
import RPi.GPIO as GPIO
import time

from engine.face_filters.face_detector import FaceDetector
from engine.face_filters.face_addons import FaceFilters
from engine.edges.edge_processor import edge_processor
from engine.finger.fingers.finger_processor import finger_processor
gpio_pin = 14
vs = cv2.VideoCapture(0)
fd = FaceDetector(True, True, False, True, True)
fa = FaceFilters()
funs = [lambda x: edge_processor(x), lambda x: fd.procces_img(x), lambda x: finger_processor(x), lambda x: fa.draw_moustache(x)]

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
f = len(funs)
i=1
while i>0:
    _,frame = vs.read()
    if GPIO.input(gpio_pin):
        i += 1
    im = funs[i%f]
    cv2.imshow("Frame", im)
    key = cv2.waitKey(1) & 0xFF
