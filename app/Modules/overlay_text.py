import cv2
import numpy as np

class OverlayText:
    def __init__(self, text:list[str], x:int, y:int, font, color:tuple[int,int,int]):
        self.text = text
        self.x = x
        self.y = y
        (self.text_width,self.text_height),self.text_first_baseline = cv2.getTextSize(self.get_longest_line(), font, 1, 1)
        self.font = font
        self.color = color
        self.visible = True
        self.background_color = (0, 0, 0)
        self.transparency = 0.5
        self.text_transparency = 0.5
        self.print_once=1

    def set_text(self, text:list[str]):
        self.text = text
        (self.text_width, self.text_height),self.text_first_baseline = cv2.getTextSize(self.get_longest_line(), self.font, 1, 1)

    def draw(self, frame):
        if not self.visible:
            return
        text_area = frame[self.y:self.y + 2*self.text_height*(len(self.text)+1), self.x:self.x + self.text_width]
        label_area = np.full(text_area.shape, self.background_color, dtype=np.uint8)
        cv2.addWeighted(text_area, self.transparency, label_area, 1 - self.transparency, 0, text_area)
        
        for i, line in enumerate(self.text):
            cv2.putText(text_area, line, (0, (2*(i+1)*self.text_height)), self.font, self.text_transparency, self.color, 1)
        
        frame[self.y:self.y + 2*self.text_height*(len(self.text)+1), self.x:self.x + self.text_width] = text_area
        
            # label_area = frame[self.y:self.y + self.height, self.x:self.x + self.width]
            
            # color_rect = np.full(label_area.shape, self.background_color, dtype=np.uint8)
            # cv2.rectangle(label_area, (0, 0), (self.width, 20), self.background_color, -1)
            # cv2.addWeighted(label_area, self.transparency, color_rect, 1 - self.transparency, 0, label_area)
            # cv2.putText(label_area, line, (0, 15), self.font, self.text_transparency, self.color, 1)
            # frame[self.y:self.y + self.height, self.x:self.x + self.width] = label_area
    
    def  get_longest_line(self):
        longest_line = ""
        for line in self.text:
            if len(line) > len(longest_line):
                longest_line = line
        return longest_line
        
        