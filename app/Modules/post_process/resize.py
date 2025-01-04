import cv2
from .post_processor import PostProcessor

class Resize(PostProcessor):
    def __init__(self, width, height):
        super().__init__()
        self.__name__ = "Resize"
        self.width = width
        self.height = height

    def apply(self, frame):
        if self.width <= 0 or self.height <= 0 or frame is None:
            return frame
        if frame.shape[0] == self.height and frame.shape[1] == self.width:
            return frame
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            return frame
        if self.width == None or self.height == None:
            return frame
        return cv2.resize(frame, (self.width, self.height))