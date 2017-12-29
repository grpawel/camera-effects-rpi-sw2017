import cv2
#parts of face definistions
face_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('./res/haarcascades/haarcascade_smile.xml')
mouth_cascade = cv2.CascadeClassifier('./res/haarcascades/Mouth.xml')
nose_cascade = cv2.CascadeClassifier('./res/haarcascades/Nose.xml')

blue = (255,0,0)
green = (0, 255, 0)
red = (0,0,255)
yellow = (0,255,255)

def draw_rectange_on_face(img, face):
    x,y, width, height = face
    img = cv2.rectangle(img,(x,y), (x+width, y+height), blue,5)
    return img

import os
import numpy as np


def draw_rectange_on_eye(img, eye):
    x, y, width, height = eye
    img = cv2.rectangle(img, (x, y), (x + width, y + height), green, 5)
    return img


def draw_rectange_on_smile(img, smile):
    pass


def draw_rectange_on_mouth(img, mouth):
    x, y, width, height = mouth
    color = (255, 255, 0)
    img = cv2.rectangle(img, (x, y), (x + width, y + height), yellow, 1)
    return img


def draw_rectange_on_nose(img, nose):
    x, y, width, height = nose
    color = (0, 0, 255)
    img = cv2.rectangle(img, (x, y), (x + width, y + height), color, 1)
    return img


def face_detector(img, faces=True, eyes=False, smiles=False, mouths=False, noses=False):
    scale = 1.3
    min_neighbours = 5

    # convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if faces:
        for face in face_cascade.detectMultiScale(gray,scale, min_neighbours):
            img = draw_rectange_on_face(img, face)
    if eyes:
        for eye in eyes_cascade.detectMultiScale(gray,scale, min_neighbours):
            img = draw_rectange_on_eye(img, eye)
    if smiles:
        for smile in smile_cascade.detectMultiScale(gray,scale, min_neighbours):
            img = draw_rectange_on_smile(img,smile)
    if mouths:
        for mouth in mouth_cascade.detectMultiScale(gray,1.7, 11):
            img = draw_rectange_on_mouth(img, mouth)
    if noses:
        for nose in nose_cascade.detectMultiScale(gray,scale, min_neighbours):
            img = draw_rectange_on_nose(img, nose)
    return img



