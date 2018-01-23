import cv2


class NoiseRemover():
    def __init__(self):
        self.kernel_sizes = [3, 5, 7, 9]
        self.current_kernel = 0

    def remove_noise(self, frame):
        frame = cv2.medianBlur(frame, self.kernel_sizes[self.current_kernel])
        return 'Remove noise', frame

    def next(self):
        self.current_kernel = (self.current_kernel + 1) % len(self.kernel_sizes)
