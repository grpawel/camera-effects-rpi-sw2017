import cv2
import numpy as np
import math
import time


def finger_processor(img):
    cv2.rectangle(img, (500, 500), (100, 100), (0, 255, 0), 0)
    crop_img = img[100:500, 100:500]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                                                  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key=lambda x: cv2.contourArea(x))
    hull = cv2.convexHull(cnt)

    drawing = np.zeros(crop_img.shape, np.uint8)
    hull = cv2.convexHull(cnt, returnPoints=False)

    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)

        cv2.line(crop_img, start, end, [0, 255, 0], 2)
        # cv2.circle(crop_img,far,5,[0,0,255],-1)

    # define actions required
    print(count_defects)
    return 'finger', img
