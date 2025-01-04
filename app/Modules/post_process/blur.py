import cv2
from .post_processor import PostProcessor

class Blur(PostProcessor):
    def __init__(self):
        super().__init__()
        self.__name__ = "Blur"

    def apply(self, frame):
        if frame is None:
            return None
        return cv2.GaussianBlur(frame, (21, 21), 0)