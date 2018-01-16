import cv2


class Inverter():
    def invert(self, frame):
        frame = cv2.bitwise_not(frame)
        return 'Invert', frame
