import cv2
from .post_processor import PostProcessor

class Invert(PostProcessor):
    def __init__(self):
        super().__init__()
        self.__name__ = "Invert"
    
    def apply(self, image):
        return cv2.bitwise_not(image)