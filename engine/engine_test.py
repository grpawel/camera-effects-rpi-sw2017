import cv2
import RPi.GPIO as GPIO
import time

from face_filters.face_detector import FaceDetector
from face_filters.face_addons import FaceFilters
from edges.edge_processor import edge_processor
from finger.fingers.finger_processor import finger_processor
from object_tracking.tracker import ObjectTracker
import numpy as np
gpio_pin = 15
vs = cv2.VideoCapture(0)
fd = FaceDetector(True, True, False, False, False)
fa = FaceFilters()
ob = ObjectTracker(np.array([30, 150, 50]), np.array([255, 255, 255]))
funs = [edge_processor, fd.procces_img, fa.draw_moustache, fa.draw_hat, ob.process]


GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
f = len(funs)
i=0
fun = funs[0]
last_change = time.time()
def change_func(_):
    global i
    global last_change
    global fun
    global funs
    current_time = time.time()
    if current_time - last_change >= 0.5:
        i += 1
        fun = funs[i%f]
        last_change = current_time
        cv2.destroyAllWindows()
def exit_func(_):
    exit()
    
GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=change_func)
GPIO.add_event_detect(18, GPIO.FALLING, callback=exit_func)
while True:
    _,frame = vs.read()
    print(i)
    name, im = fun(frame)
    cv2.imshow(name, im)
    key = cv2.waitKey(1) & 0xFF
