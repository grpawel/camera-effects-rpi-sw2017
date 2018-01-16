import cv2


class NoiseRemover():
    def remove_noise(self, frame):
        frame = cv2.medianBlur(frame, 10)
        return 'Remove noise', frame
