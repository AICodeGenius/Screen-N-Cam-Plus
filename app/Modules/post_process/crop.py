from .post_processor import PostProcessor

class Crop(PostProcessor):
    def __init__(self, x, y, width, height):
        if x < 0 or y < 0 or width < 0 or height < 0:
            raise ValueError("Invalid crop parameters")
        self.__init__()
        self.__name__ = "Crop"
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def apply(self, frame):
        if frame is None:
            return None
        return frame[self.y:self.y+self.height, self.x:self.x+self.width]