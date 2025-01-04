import cv2
from .post_processor import PostProcessor

class Dilate(PostProcessor):
    def __init__(self, kernel_size=5,iterations=1):
        super().__init__()
        self.__name__ = "Dilate"
        self.kernel_size = kernel_size
        self.iterations = iterations

    def process(self, frame):
        if frame is None:
            return None
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_size, self.kernel_size))
        return frame
    
    def apply(self, frame):
        if frame is None:
            return None
        return cv2.erode(frame, self.kernel, self.iterations)