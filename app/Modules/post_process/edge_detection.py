import cv2
from .post_processor import PostProcessor

class EdgeDetection(PostProcessor):
    def __init__(self, threshold1=100, threshold2=200):
        super().__init__()
        self.__name__ = "EdgeDetection"
        self.threshold1 = threshold1
        self.threshold2 = threshold2
    
    def apply(self, frame):
        if frame is None:
            return None
        return cv2.Canny(frame, self.threshold1, self.threshold2)