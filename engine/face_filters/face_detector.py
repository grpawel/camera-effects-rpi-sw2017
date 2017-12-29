import cv2
def draw_rectange_on_face(img, face):
    x,y, width, height = face
    color = (255,0,0)
    img = cv2.rectangle(img,(x,y), (x+width, y+height), color,5)
    return img

import os
import numpy as np
def face_detector(img):
    scale = 1.3
    min_neighbours = 5
    files = [f for f in os.listdir('..') if os.path.isfile(f)]
    for f in files:
        print(f)
    #load faces and eyes definition
    face_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_frontalface_default.xml')
    # convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for face in face_cascade.detectMultiScale(gray,scale, min_neighbours):
        img = draw_rectange_on_face(img, face)
    return img


