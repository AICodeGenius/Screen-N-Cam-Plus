import cv2
from .post_processor import PostProcessor

class Sharpen(PostProcessor):
    def __init__(self, kernel_size=3):
        super().__init__()
        self.__name__ = "Sharpener"
        self.kernel_size = kernel_size

    def process(self, image):
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.kernel_size, self.kernel_size))
        return image
    
    def apply(self, image):
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, self.kernel)
        #return cv2.filter2D(image, -1, self.kernel)