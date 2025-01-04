import cv2
import numpy as np
from .post_processor import PostProcessor

class TextOverlay(PostProcessor):
    def __init__(self, text, position,background_color=(255, 255, 255), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(0, 0, 0), thickness=2):
        super().__init__()
        self.__name__ = "TextOverlay"
        self.__font = font
        self.position = position
        self.background_color = background_color
        self.__font_scale = font_scale
        self.color = color
        self.__thickness = thickness
        self.transparency = 0.2
        self.text_transparency = 0.5
        self.set_text(text)

    def set_text(self, text):
        self.__text = text
        (self.text_width, self.text_height),self.text_first_baseline = cv2.getTextSize(self.__text, self.__font, self.__font_scale, self.__thickness)

    def get_text(self):
        return self.__text
    
    def get_font(self)->tuple[int,int,int]:
        return self.__font,self.__font_scale,self.__thickness

    def apply(self, frame):
        if frame is None:
            return None
        x = self.position[0]
        y = self.position[1]
        w = self.text_width + int(self.text_width*0.3+1)
        h = self.text_height*2
        if x+w > frame.shape[1]:
            w = frame.shape[1] - x
        if y+h > frame.shape[0]:
            h = frame.shape[0] - y
        text_area = frame[y:y+h, x:x+w]
        label_area = np.full(text_area.shape, self.background_color, dtype=np.uint8)
        cv2.addWeighted(text_area, self.transparency, label_area, 1 - self.transparency, 0, text_area)
        cv2.putText(text_area, self.__text, (self.position[1],self.position[0]+self.text_first_baseline), self.__font, self.__font_scale, self.color, self.__thickness)
        frame[y:y+h, x:x+w] = text_area
        return frame