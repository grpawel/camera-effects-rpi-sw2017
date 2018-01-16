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
        self.moustache = cv2.imread('./res/moustache.png',-1)
    def draw_moustache(self, img):
        if self.nose_live < 0:
            if self.nose_live < -7:
                self.nose_centres = []
            noses = self.face_detector.find_nose_list(img)
            if len(noses) > 0:
                self.nose_live = 1
                self.nose_centres = noses
                for nose in self.nose_centres:
                    fy = 2.5 * nose[2] / self.moustache.shape[1]
                    mous = cv2.resize(self.moustache, None, fx=fy, fy=fy)
                    nose[3] = mous
        for nose in self.nose_centres:

            self.draw_effect(img,nose[3],nose[0], nose[1]+20)

        self.nose_live-=1
        return img

    def draw_effect(self, frame, effect, x_center, y_center):
        (h, w) = (effect.shape[0], effect.shape[1])
        (imgH, imgW) = (frame.shape[0], frame.shape[1])
        y_offset = y_center
        x_offset = x_center - w//2

        if y_offset + h >= imgH:  # if sprite gets out of image in the bottom
            effect = effect[0:imgH - y_offset, :, :]

        if x_offset + w >= imgW:  # if sprite gets out of image to the right
            effect = effect[:, 0:imgW - x_offset, :]

        if x_offset < 0:  # if sprite gets out of image to the left
            sprite = effect[:, abs(x_offset)::, :]
            w = sprite.shape[1]
            x_offset = 0

        # for each RGB chanel
        for c in range(3):
            # chanel 4 is alpha: 255 is not transpartne, 0 is transparent background
            frame[y_offset:y_offset + h, x_offset:x_offset + w, c] = \
                effect[:, :, c] * (effect[:, :, 3] / 255.0) + frame[y_offset:y_offset + h, x_offset:x_offset + w, c] * (
                1.0 - effect[:, :, 3] / 255.0)
        return frame




