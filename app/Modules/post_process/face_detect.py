from typing import Sequence
import cv2
import cv2.data
from cv2.typing import Rect
import threading
from datetime import datetime
from .post_processor import PostProcessor

class FaceDetection(PostProcessor):
    def __init__(self, cascade_path=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'):
        super().__init__()
        self.__name__="Face Detection"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.faces:Sequence[Rect] = None
        self.__is_processing__ = False
        self.__detected_time__ = datetime.now().replace(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def is_detected(self) -> tuple[float,int]:
        return (datetime.now() - self.__detected_time__).total_seconds(),len(self.faces) if self.faces is not None else 0

    def __process(self, frame):
        if frame is None:
            self.__is_processing__ = False
            return
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.medianBlur(gray, 5)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5,minSize=(40,40))
        self.__is_processing__ = False
        if len(faces) > 0:
            self.faces = faces
            self.__detected_time__ = datetime.now()

    def process(self, frame):
        if(self.__is_processing__):
            return
        self.__is_processing__ = True
        threading.Thread(target=self.__process, args=(frame,)).start()        
        
    def apply(self, frame):
        if(self.faces is None):
            return frame
        for (x, y, w, h) in self.faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return frame
