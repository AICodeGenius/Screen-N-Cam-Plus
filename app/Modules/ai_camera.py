import cv2
import threading
from camera_config import CameraConfig
from feed_provider import FeedProvider
from typing import Final

class AICamera:
    __streaming__:bool = False
    __id__:Final[int] 
    config:Final[CameraConfig]

    def __init__(self, camera_id=0):
        self.__streaming__ = False
        self.__id__ = camera_id
        self.camera = cv2.VideoCapture(camera_id)
        if not self.camera.isOpened():
            raise ValueError("Unable to open camera")
        self.config = CameraConfig(camera_id, self.camera)
        #self.config.set_resolution((640,480))
        self.camera.release()
        self.__thread = None

    def get_id(self):
        return self.__id__
    
    def get_frame_size(self):
        return self.__frame_size

    def frame(self):
        self.camera = cv2.VideoCapture(0)
        while self.__streaming__:
            ret, frame = self.camera.read()
            if not ret:
                break
            yield frame
        self.camera.release()
    
    def __frame(self, shared_store:FeedProvider):
        self.camera = cv2.VideoCapture(0)
        while self.__streaming__:
            ret, frame = self.camera.read()
            if not ret:
                continue
            shared_store.put(frame)
        self.camera.release()

    def start_stream(self,shared_store):
        self.__thread = threading.Thread(target=self.__frame,args=(shared_store,))
        self.__thread.start()
        self.__streaming__ = True
    
    def stop_stream(self):
        self.__streaming__ = False
        self.__thread.join()
        self.camera.release()

    def is_streaming(self):
        return self.__streaming__

    def  get_config(self):
        return self.config
    
    def __del__(self):
        self.stop_stream()
        self.camera.release()
    
    def __enter__(self):
        self.start_stream()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_stream()
        self.camera.release()

    def __iter__(self):
        return self.frame()
    
    def __next__(self):
        return next(self.frame())
    
    def __len__(self):
        return 1

#Test threading
if __name__ == "__main__":
    shared_store = FeedProvider()
    cam = AICamera(0)
    cam.get_config().turn_on_metrics()
    cam.start_stream(shared_store)
    frame = shared_store.get()
    prev_frame=frame
    while True:
        try:
            frame = shared_store.get(block=False)
        except:
            frame = prev_frame
        cv2.imshow("Frame", frame)
        prev_frame = frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.stop_stream()
    cv2.destroyAllWindows()

    
    
