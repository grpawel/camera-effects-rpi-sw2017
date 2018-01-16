from collections import deque
import cv2
import imutils as imutils



class ObjectTracker():
    def __init__(self, down,up):
        self.TRACES = 10
        self.object_colour_rgb_bound_down = down
        self.object_colour_rgb_bound_up = up
        self.centres = [None for i in range(0, self.TRACES)]
        self.trace_start = 0
        self.trace_live = 0
        self.x = None
        self.y = None
        self.radius = None
        self.resize_scale = 0.3


    def process(self, img):

        working_frame = cv2.resize(img,None,fx=self.resize_scale, fy=self.resize_scale)
        if self.trace_live > 0:
            cv2.circle(img, (int(self.x), int(self.y)), int(self.radius),
                       (0, 255, 255), 2)
            cv2.circle(img, self.center, 5, (0, 0, 255), -1)
            trace_size = 10
            traces = self.centres[-(self.TRACES - self.trace_start):] + self.centres[:self.trace_start]
            for trace in reversed(traces):
                trace_size = int(0.98 * trace_size)
                cv2.circle(img, trace, trace_size, (0, 0, 255), -1)
            self.trace_live-=1
        else:
            cv2.GaussianBlur(working_frame, (11, 11), 0)
            hsv = cv2.cvtColor(working_frame, cv2.COLOR_BGR2HSV)
            mask = self.build_mask(hsv)
            counturs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if len(counturs) > 0:
                c = max(counturs, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                self.x = int(x/self.resize_scale)
                self.y = int(y/self.resize_scale)
                self.radius = int(radius/self.resize_scale)
                M = cv2.moments(c)
                center = tuple(map(lambda x: int(x/self.resize_scale),(int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))))
                self.center = center
                self.centres[self.trace_start] = center
                self.trace_start = (self.trace_start + 1) % self.TRACES

                self.trace_live = 5

        return 'Tracker', img

    def build_mask(self, hsv):
        mask = cv2.inRange(hsv, self.object_colour_rgb_bound_down, self.object_colour_rgb_bound_up)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask


