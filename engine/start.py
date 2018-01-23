import time

import RPi.GPIO as GPIO
import cv2
from basic.invert import Inverter
from basic.remove_noise import NoiseRemover
from edges.edge_processor import edge_processor
from face_filters.face_addons import FaceFilters
from face_filters.face_detector import FaceDetector
from finger.fingers.finger_processor import finger_processor
from object_tracking.tracker import ObjectTracker

# Buttons GPIO pins
# Button A - for selecting effect
BUTTON_A_GPIO_PIN = 15
# Button B - for selecting parameters
BUTTON_B_GPIO_PIN = 18

# Button debounce
BUTTON_DEBOUNCE = 0.5

fd = FaceDetector(True, True, False, False, False)
fa = FaceFilters()
ob = ObjectTracker()
inv = Inverter()
nr = NoiseRemover()

# List of image processing function, and change param func
funs = [(edge_processor, None), (fd.procces_img, fd.next), (fa.draw_moustache, None), (fa.draw_hat, None),
        (ob.process, ob.next), (finger_processor, None), (inv.invert, None), (nr.remove_noise, nr.next)]

f = len(funs)
i = 0
fun = funs[0]
last_change_a = time.time()
fun_changed = False


def change_func(_):
    global i
    global last_change_a
    global fun
    global funs
    global fun_changed
    current_time = time.time()
    if current_time - last_change_a >= BUTTON_DEBOUNCE:
        i += 1
        fun = funs[i % f]
        last_change_a = current_time
        fun_changed = True

last_change_b = time.time()


def change_param(_):
    global fun
    global last_change_b
    if fun[1] is not None:
        current_time = time.time()
        if current_time - last_change_b >= BUTTON_DEBOUNCE:
            fun[1]()
            last_change_b = current_time



def setup_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_A_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_B_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_A_GPIO_PIN, GPIO.FALLING, callback=change_func)
    GPIO.add_event_detect(BUTTON_B_GPIO_PIN, GPIO.FALLING, callback=change_param)

setup_buttons()

time.sleep(2)
vs = cv2.VideoCapture(0)
time.sleep(1)

fails = 0
while fails < 3:
    _, frame = vs.read()
    if frame is None:
        print('Can not retrieve image from camera. Check whether it is not detached or busy.')
        print('Next try in 1 second.')
        fails += 1
        time.sleep(1)
    else:
        name, im = fun[0](frame)
        cv2.imshow(name, im)
        key = cv2.waitKey(1) & 0xFF
        if fun_changed:
            cv2.destroyAllWindows()
            fun_changed = False
