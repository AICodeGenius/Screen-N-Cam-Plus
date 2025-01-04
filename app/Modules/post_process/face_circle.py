import cv2
import numpy as np
from .face_crop import FaceCrop

class FaceCircle(FaceCrop):
    def __init__(self, padding=0.8):
        super().__init__(padding, maintain_aspect=True)
        self.__name__="Face Lasso"
        self.__lasso__ = None
        self.__lasso_points__ = None
        self.__lasso_mask__ = None
        self.__lasso_masked__ = None
        self.__lasso_masked_frame__ = None
        self.__lasso_masked_frame__ = None
        self.__lasso_masked_frame__ = None
   
    def __create_lasso_mask(self, frame, faces):
        if len(faces) == 0:
            return None
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        for (x, y, w, h) in faces:
            cv2.ellipse(mask, (int(x + w / 2), int(y + h / 2)), (int(w / 2)*2, int(h / 2)*2), 0, 0, 360, 255, -1)
        return mask
    
    def __create_lasso_masked(self, frame, mask):
        if mask is None:
            return None
        return cv2.bitwise_and(frame, frame, mask=mask)
    
    def apply(self, frame):
        if frame is None:
            return None
        if self.faces is None:
            return frame
        self.__lasso_mask__ = self.__create_lasso_mask(frame, self.faces)
        self.__lasso_masked__ = self.__create_lasso_masked(frame, self.__lasso_mask__)
        frame = self.__lasso_masked__[~np.all(self.__lasso_masked__==0, axis=(1,2))]
        frame=cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = frame[~np.all(frame==0, axis=(1,2))]
        frame=cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return frame