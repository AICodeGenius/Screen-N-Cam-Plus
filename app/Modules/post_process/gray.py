import cv2
from .post_processor import PostProcessor

    
class Grey(PostProcessor):
    def __init__(self):
        super().__init__()
        self.__name__ = "Grey"
    
    def apply(self, frame):
        if frame is None:
            return None
        try:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            return frame
