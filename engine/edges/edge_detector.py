import numpy as np
import cv2
from engine.engine_main import BaseTarget


class EdgeDetector(BaseTarget):
    def __init__(self, ):
        pass

    def process(self, img):
        gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        b = cv2.GaussianBlur(gr, (3, 3), 0)
        v = np.median(b)
        lower = int(max(0, (0.66) * v))
        upper = int(min(255, (1.33) * v))
        return cv2.Canny(b, lower, upper)
