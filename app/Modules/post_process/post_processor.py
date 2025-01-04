
class PostProcessor:
    def __init__(self) -> None:
        self.__name__="None"

    def get_name(self):
        return self.__name__

    def process(self, frame): # Keyframes only
        return frame
    
    def apply(self, frame): # Applied on all frames
        return frame

    
