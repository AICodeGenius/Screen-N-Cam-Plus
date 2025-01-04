
# Filter modes
from typing import Final
import cv2
from datetime import datetime


NONE = 0       # Preview mode
BLUR = 1          # Blur mode
FEATURES = 2      # Features mode
CANNY = 3         # Canny mode
GRAYSCALE = 4     # Grayscale mode
LAPLACIAN = 5     # Laplacian edge detection mode
THRESHOLD = 6     # Threshold mode
BILATERAL = 7     # Bilateral filtering mode

filter_modes:Final = {
    NONE: "None",
    BLUR: "Blur",
    FEATURES: "Features",
    CANNY: "Canny",
    GRAYSCALE: "Grayscale",
    LAPLACIAN: "Laplacian",
    THRESHOLD: "Threshold",
    BILATERAL: "Bilateral"
}

class CameraConfig:

    def __init__(self,camera_id:int,video:cv2.VideoCapture) -> None:
        self.reset()
        self.frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_size = (self.frame_width, self.frame_height)
        self.fps = int(video.get(cv2.CAP_PROP_FPS))
        self.fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
        self.camera_id = camera_id
        self.camera_name = "Camera " + str(camera_id)
        self.camera_resolution = (self.frame_width, self.frame_height)
        self.camera_format = self.fourcc

    def set_camera_name(self, name:str):
        self.camera_name = name

    def reset(self):
        self.turn_off_metrics()
        self.filter=filter_modes[NONE]
        self.flip_camera = False
        
    def set_filter(self, filter:int):
        self.filter = filter_modes[filter]
    
    def remove_filter(self):
        self.filter = filter_modes[NONE]

    def flip(self):
        self.flip_camera = True
    
    def unflip(self):
        self.flip_camera = False

    def toggle_flip(self):
        self.flip_camera = not self.flip_camera

    def set_fps(self, fps:int):
        self.fps = fps
        
    def set_resolution(self, resolution:tuple[int,int]):
        self.frame_width = resolution[0]
        self.frame_height = resolution[1]
        self.frame_size = (self.frame_width, self.frame_height)

    def turn_on_metrics(self):
        self.show_fps = True
        self.show_timestamp = True
        self.show_camera_id = True
        self.show_camera_resolution = True
        self.show_camera_format = True

    def turn_off_metrics(self):
        self.show_fps = False
        self.show_timestamp = False
        self.show_camera_id = False
        self.show_camera_resolution = False
        self.show_camera_format = False
    
    def get_config_text(self)->str:
        ret:list[str] = []
        if self.show_fps:
            ret.append("FPS: " + str(self.fps))
        if self.show_timestamp:
            ret.append("Time: " + datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        if self.show_camera_id:
            ret.append("Camera ID: " + str(self.camera_id) + "("+ self.camera_name + ")")
        if self.show_camera_resolution:
            ret.append("Camera Resolution: " + str(self.camera_resolution))
        if self.show_camera_format:
            ret.append("Camera Format: " + str(self.camera_format))
        if self.flip_camera:
            ret.append("Flip Camera: " + str(self.flip_camera))
        return ret
    