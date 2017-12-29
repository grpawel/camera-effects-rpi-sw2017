import cv2
cap = cv2.VideoCapture(0)
from engine.edges.edge_processor import edge_processor

while True:
    _,frame = cap.read()
    im = edge_processor(frame)
    cv2.imshow('frame', im)
    key = cv2.waitKey(1) & 0xFF
