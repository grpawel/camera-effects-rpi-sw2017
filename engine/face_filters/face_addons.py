from face_filters.face_detector import FaceDetector
import cv2
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
yellow = (0, 255, 255)
orange = (0,140,255)


class FaceFilters:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.nose_centres = []
        self.nose_live = 1
    def draw_moustache(self, img):
        if self.nose_live < 0:
            if self.nose_live < -7:
                self.nose_centres = []
            noses = self.face_detector.find_nose_list(img)
            if len(noses) > 0:
                self.nose_live = 1
                self.nose_centres = noses
        for nose in self.nose_centres:
            cv2.circle(img, (nose[0],nose[1]), 10, (0, 0, 255), 2)
        self.nose_live-=1
        return img



