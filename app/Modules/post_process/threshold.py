import cv2
from .post_processor import PostProcessor

class Threshold(PostProcessor):
    def __init__(self, threshold=127, max_value=255, type=cv2.THRESH_BINARY):
        super().__init__()
        self.__name__ = "Threshold"
        self.threshold = threshold
        self.max_value = max_value
        self.type = type
    
    def apply(self, image):
        return cv2.threshold(image, self.threshold, self.max_value, self.type)