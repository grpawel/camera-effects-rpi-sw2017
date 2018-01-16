import cv2
import numpy as np

def edge_processor(img):
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b = cv2.GaussianBlur(gr, (3, 3), 0)
    v = np.median(b)
    lower = int(max(0, (0.66) * v))
    upper = int(min(255, (1.33) * v))
    return 'edge', cv2.Canny(b, lower, upper)