import cv2
import RPi.GPIO as GPIO
import time

from face_filters.face_detector import FaceDetector
from face_filters.face_addons import FaceFilters
from edges.edge_processor import edge_processor
from finger.fingers.finger_processor import finger_processor
from object_tracking.tracker import ObjectTracker
from basic.invert import Inverter
from basic.remove_noise import NoiseRemover
import numpy as np

gpio_pin = 15
vs = cv2.VideoCapture(0)
fd = FaceDetector(True, True, False, False, False)
fa = FaceFilters()
ob = ObjectTracker(np.array([30, 150, 50]), np.array([255, 255, 255]))
inv = Inverter()
nr = NoiseRemover()
# list of image processing function, and change param func
funs = [(edge_processor, None), (fd.procces_img, fd.next), (fa.draw_moustache, None), (fa.draw_hat, None),
        (ob.process, ob.next), (finger_processor, None), (inv.invert, None), (nr.remove_noise, None)]

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
f = len(funs)
i = 0
fun = funs[0]
last_change = time.time()
fun_changed = False


def change_func(_):
    global i
    global last_change
    global fun
    global funs
    global fun_changed
    current_time = time.time()
    if current_time - last_change >= 0.5:
        i += 1
        fun = funs[i % f]
        last_change = current_time
        fun_changed = True


def change_param(_):
    if fun[1] is not None:
        fun[1]()


GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=change_func)
GPIO.add_event_detect(18, GPIO.FALLING, callback=change_param)
while True:
    _, frame = vs.read()
    name, im = fun[0](frame)
    cv2.imshow(name, im)
    key = cv2.waitKey(1) & 0xFF
    if fun_changed:
        cv2.destroyAllWindows()
        fun_changed = False
