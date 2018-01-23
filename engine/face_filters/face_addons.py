import cv2
from face_filters.face_detector import FaceDetector

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
yellow = (0, 255, 255)
orange = (0, 140, 255)


class FaceFilters:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.nose_centres = []
        self.nose_live = 1
        self.head_Live = 1
        self.head_top_centres = []
        self.moustache = cv2.imread('/home/pi/projects/sw/camera-effects-rpi-sw2017/engine/res/moustache.png', -1)
        self.hat = cv2.imread('/home/pi/projects/sw/camera-effects-rpi-sw2017/engine/res/christmas_hat.png', -1)

    def draw_moustache(self, img):
        if self.nose_live < 0:
            if self.nose_live < -7:
                self.nose_centres = []
            noses = self.face_detector.find_nose_list(img)
            if len(noses) > 0:
                self.nose_live = 5
                self.nose_centres = noses
                for nose in self.nose_centres:
                    fy = 2.5 * nose[2] / self.moustache.shape[1]
                    mous = cv2.resize(self.moustache, None, fx=fy, fy=fy)
                    nose[3] = mous
        for nose in self.nose_centres:
            self.draw_effect(img, nose[3], nose[0], nose[1] + 20)

        self.nose_live -= 1
        return 'moustache', img

    def draw_hat(self, img):
        if self.head_Live < 0:
            if self.head_Live < -7:
                self.head_top_centres = []
            heads = self.face_detector.find_head_list(img)
            if len(heads) > 0:
                self.head_Live = 10
                self.head_top_centres = heads
                for head in self.head_top_centres:
                    fy = 1.3 * head[2] / self.hat.shape[1]
                    hat = cv2.resize(self.hat, None, fx=fy, fy=fy)
                    head[3] = hat
        for head in self.head_top_centres:
            cv2.circle(img, (head[0], head[1]), int(5),
                       (0, 255, 255), 2)
            self.draw_effect(img, head[3], head[0] + int(int(head[3].shape[1] // 5)),
                             head[1] - int(head[3].shape[0] // 1.5))
        self.head_Live -= 1
        return 'hat', img

    def draw_effect(self, frame, effect, x_center, y_center):
        (h, w) = (effect.shape[0], effect.shape[1])
        (imgH, imgW) = (frame.shape[0], frame.shape[1])
        if y_center < 0:
            x_offset = x_center - w // 2
            y_offset = 0
        else:
            x_offset = x_center - w // 2
            y_offset = y_center

        if y_offset + h >= imgH:
            effect = effect[0:imgH - y_offset, :, :]

        if x_offset + w >= imgW:
            effect = effect[:, 0:imgW - x_offset, :]

        if x_offset < 0:
            sprite = effect[:, abs(x_offset)::, :]
            w = sprite.shape[1]
            x_offset = 0

        # for each RGB chanel
        for c in range(3):
            frame[y_offset:y_offset + h, x_offset:x_offset + w, c] = \
                effect[:, :, c] * (effect[:, :, 3] / 255.0) + frame[y_offset:y_offset + h, x_offset:x_offset + w, c] * (
                    1.0 - effect[:, :, 3] / 255.0)
        return frame
