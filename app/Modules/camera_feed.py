from feed_provider import FeedProvider
from ai_camera import AICamera
import numpy as np

class CameraFeed(FeedProvider):
    def __init__(self, camera:AICamera):
        super().__init__()
        self.camera = camera
        if self.camera is None:
            raise ValueError("Camera not initialized")
        #self.camera.start_stream(self)
    
    def start_stream(self):
        self.camera.start_stream(self)
        return self
    
    def get(self):
        frame = super().get()
        if frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        return self.camera.is_streaming(),frame
    
    def __del__(self):
        self.camera.stop_stream()
        self.camera.camera.release()

    def __enter__(self):
        self.camera.start_stream(self)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.camera.stop_stream()
        self.camera.camera.release()
