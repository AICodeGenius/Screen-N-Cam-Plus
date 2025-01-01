import cv2
import numpy as np

MAX_CAMERAS=10

class CameraGroup:
    __capture_size__ = None

    class Camera:
        def __init__(self, camera_id=0):
            self.camera_id = camera_id
            self.cap = cv2.VideoCapture(self.camera_id)

        def __generate_empty_frame(self,text:str):
            image = np.zeros(self.capture_size(), dtype = np.uint8)
            cv2.putText(image, text, (1920//2,1080//2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            return image

        def frame(self):
            if not self.cap.isOpened():
                return self.__generate_empty_frame(f"Camera {self.camera_id} is unavailable")
            ret, frame = self.cap.read()
            if not ret:
                return self.__generate_empty_frame(f"Cannot access camera {self.camera_id}")
            return frame

        def release(self):
            self.cap.release()
        
        def capture_size(self):
            if not self.cap.isOpened():
                return None
            return (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def __init__(self):
        self.cameras = []
    
    def capture_size(self):
        return (self.__capture_size__[0]*2,self.__capture_size__[1])

    def add_camera(self, camera_id=0):
        camera = self.Camera(camera_id)
        self.cameras.append(camera)
        if self.__capture_size__ is None:
            self.__capture_size__ = camera.capture_size()
        if camera.capture_size()[0]>self.__capture_size__[0]:
            self.__capture_size__ = camera.capture_size()
        return camera
    
    def all_cameras(self):
        return self.cameras
    
    def get_camera(self, camera_id=0)->Camera:
        for camera in self.cameras:
            if camera.camera_id == camera_id:
                return camera
        return None
    
    def frame(self, camera_id=0):
        camera = self.get_camera(camera_id)
        if camera:
            return camera.frame()
        return None
    
    def frames(self):
        frames = {}
        for camera in self.cameras:
            frames[camera.camera_id] = camera.frame()
        return frames
    
    def get_as_single_frame(self):
        frames = self.frames()
        if len(frames) == 0:
            return None
        if len(frames) == 1:
            return list(frames.values())[0]
        # return cv2.resize(list(frames.values())[0], self.__capture_size__)
        if len(frames) > 1:
            for i in frames:
                if frames[i] is None:
                    frames[i] = cv2.imread("assets/no_camera.png")
                    frames[i] = cv2.resize(frames[i], self.__capture_size__)
                    continue
                frames[i] = cv2.resize(frames[i], self.__capture_size__) 
        frame = frames[0]
        for i in range(1, len(frames)):
            frame = cv2.hconcat([frame, frames[i]])
        return frame
    
    def release_camera(self, camera_id=0):
        camera = self.get_camera(camera_id)
        if camera:
            camera.release()
            self.cameras.remove(camera)

    def release_all(self):
        for camera in self.cameras:
            camera.release()
        self.cameras = []

    def get_camera_ids(self):
        return [camera.camera_id for camera in self.cameras]
    
    def get_camera_count(self):
        return len(self.cameras)
    
    # def get_camera_info(self, camera_id=0):
    #     camera = self.get_camera(camera_id)
    #     if camera:
    #         return camera.get_info()
    #     return None

    def __del__(self):
        self.release_all()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.release_all()

    def __iter__(self):
        return self.cameras.__iter__()
    
    def __len__(self):
        return len(self.cameras)
    
    def __getitem__(self, key):
        return self.cameras[key]
    
    def __setitem__(self, key, value):
        self.cameras[key] = value

    def __delitem__(self, key):
        del self.cameras[key]

    def __contains__(self, item):
        return item in self.cameras
    
    def __reversed__(self):
        return reversed(self.cameras)
    
    def __add__(self, other):
        return self.cameras + other
    

def detect_all_cameras():    
    for i in range(MAX_CAMERAS):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            yield i