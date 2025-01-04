import cv2
from .post_processor import PostProcessor

class Contour(PostProcessor):
    def __init__(self, threshold=100, color=(0, 255, 0)):
        super().__init__()
        self.__name__ = "Contour"
        self.threshold = threshold
        self.color = color
        self.contours = None

    def apply(self, frame):
        if self.contours is None:
            return frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, t = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)
        self.contours, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, self.contours, -1, self.color, 2)
        return frame