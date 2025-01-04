from .resize import Resize

class Stretch(Resize):
    def __init__(self,ratio=1):
        super().__init__(640, 480)
        self.__name__ = "Stretch"
        self.ratio = ratio

    def process(self, frame):
        if frame is None:
            return frame
        size = frame.shape
        self.width = int(size[1] * self.ratio)
        self.height = int(size[0] * self.ratio)
        return frame
    
    def apply(self, frame):
        return super().apply(frame)