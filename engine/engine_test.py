import cv2
from numpy.matlib import eye

cap = cv2.VideoCapture(0)
from engine.edges.edge_processor import edge_processor
from engine.face_filters.face_detector import face_detector

while True:
    _,frame = cap.read()
    im = face_detector(frame, faces=True, mouths=True)
    cv2.imshow('frame', im)
    key = cv2.waitKey(1) & 0xFF
