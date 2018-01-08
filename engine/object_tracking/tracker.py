from collections import deque
import cv2
import imutils as imutils


class ObjectTracker:
    def __init__(self, down,up):
        self.TRACES = 10
        print(down,up)
        self.object_colour_rgb_bound_down = down
        self.object_colour_rgb_bound_up = up
        self.centres = [None for i in range(0, self.TRACES)]
        self.trace_start = 0


    def track(self, img):
        frame = imutils.resize(img,width = 600)
        cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = self.build_mask(hsv)
        counturs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(counturs) > 0:
            c = max(counturs, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            self.centres[self.trace_start] = center
            traces = self.centres[-(self.TRACES - self.trace_start):] + self.centres[:self.trace_start]
            self.trace_start = (self.trace_start + 1) % self.TRACES
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                trace_size = 10
                for trace in reversed(traces):
                    trace_size = int(0.98*trace_size)
                    cv2.circle(frame,trace, trace_size, (0, 0, 255), -1)
        return frame

    def build_mask(self, hsv):
        mask = cv2.inRange(hsv, self.object_colour_rgb_bound_down, self.object_colour_rgb_bound_up)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask


