from typing import Sequence
from cv2.typing import Rect
from .face_detect import FaceDetection
from PIL import Image,ImageFilter
import numpy as np

class FaceCrop(FaceDetection):
    def __init__(self, padding=0.5,maintain_aspect=True):
        super().__init__()
        self.__name__="FaceCrop"
        self.padding = padding
        self.maintain_aspect = maintain_aspect
        self.faces:Sequence[Rect] = None
        self.current_faces:Sequence[Rect] = None

    def crop(self,frame):
        if self.faces is None or frame is None:
            return frame
        min_x, min_y, max_x, max_y = self.__corners(frame,self.faces)
        return frame[min_y:max_y, min_x:max_x]

    def __corners(self, frame,faces)->tuple[int,int,int,int,int,int]:
        xs,ys=[],[]
        if self.maintain_aspect:
            x_aspect = frame.shape[1] / frame.shape[0]
            y_aspect = frame.shape[0] / frame.shape[1]
            x_padding = self.padding * x_aspect
            y_padding = self.padding * y_aspect
        else:
            x_padding = self.padding
            y_padding = self.padding
        for (x, y, w, h) in faces:
            xs.append(int(x - w * x_padding))
            xs.append(int(x + w * (1 + x_padding)))
            ys.append(int(y - h * y_padding))
            ys.append(int(y + h * (1 + y_padding)))
        return min(xs),min(ys),max(xs),max(ys)

    def apply(self, frame):
        if frame is None:
            return frame
        if(self.faces is None):
            return frame
        return self.crop(frame)