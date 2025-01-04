import time
import cv2
from feed_provider import FeedProvider
import numpy as np
from post_process import PostProcessor

"""
    PostProcess: 
    Summary: Receives frames from CameraFeed and apply filters and effects to frames

    Steps:
        Step 1: Create PostProcess to CameraFeed using PostPorcess(CameraFeed)
                e.g:
                from ai_camera import AICamera
                import post_process_functions as ppf
                
                camera_feed = CameraFeed()
                cam = AICamera(0)
                cam.get_config().turn_on_metrics()
                cam.start_stream(camera_feed)
                post_process = PostProcess(camera_feed)
                face_detector = FaceDetection()
                post_process.add(face_detector, key_frames_only=True)
                while True:
                    frame, key_frame = post_process.get_frame()
                    cam.config.set_fps(post_process.get_fps())
                    cv2.imshow("Frame", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                cam.stop_stream()
                cv2.destroyAllWindows()
                

"""
class PostProcess(dict[PostProcessor]):
    def __init__(self, camera_feed:FeedProvider):
        self.camera_feed = camera_feed
        self.__key_frame__ = None
        self.__previous_frame__=np.zeros((1920,1080,3),dtype=np.uint8)
        self.__previous_value__ = 0
        self.__last_key_frame_time__ = time.time()
        self.__frames_processed__ = 0
        self.__frames_processed_last__ = 0
        self.__frames_processed_time__ = time.time()
    
    def __calculate_frames_processed(self):
        self.__frames_processed__ += 1
        if time.time() - self.__frames_processed_time__ > 1:
            self.__frames_processed_time__ = time.time()
            self.__frames_processed_last__ = self.__frames_processed__
            self.__frames_processed__ = 0
        return self.__frames_processed_last__

    def __key_frame_time_lapsed(self):
        if self.__last_key_frame_time__:
            if time.time() - self.__last_key_frame_time__ > 1:
                self.__last_key_frame_time__ = time.time()
                return True
            else:
                return False
        else:
            self.__last_key_frame_time__ = time.time()
            return True
   
    def get_fps(self):
        return self.__frames_processed_last__    

    def get_frame(self):
        try:  
            frame = self.camera_feed.get(block=False)
            self.__previous_frame__ = frame 
        except:
            frame = self.__previous_frame__
        self.__calculate_frames_processed()
        # self.__previous_frame__ = frame
        # if self.__key_frame__ is None:
        #     self.__key_frame__ = np.zeros(frame.shape, dtype=np.uint8)
        if np.sum(frame) == 0:
            key_frame = False
            return frame, key_frame
        else:
            key_frame = self.__is_key_frame(frame)
            return self.__process_frame(frame, key_frame)

    def __process_frame(self, frame, key_frame):
        if frame is None:
            frame = self.__previous_frame__
        for item in self.keys():
            if self[item]['key_frame_only']:
                if key_frame or self.__key_frame_time_lapsed():
                    if len(self[item]['args'])>0:
                        self[item]['post_processor'].process(frame, self[item]['args'])
                    else:
                        self[item]['post_processor'].process(frame)
            else:
                if len(self[item]['args'])>0:
                    frame=self[item]['post_processor'].process(frame, self[item]['args'])
                else:
                    frame=self[item]['post_processor'].process(frame)
            frame=self[item]['post_processor'].apply(frame)
        if frame is None:
            frame = self.__previous_frame__
        return frame, key_frame

    def __is_key_frame(self, frame):
        current_value = np.sum(frame)
        key_frame=False
        if round(abs(current_value - self.__previous_value__)/current_value,4) > 0.10:
            self.__previous_value__ = current_value
            key_frame=True
        return key_frame
    
    def add(self, post_processor,key_frames_only=False,args:list=[]):
        val:dict = {}
        val['post_processor']=post_processor
        val['key_frame_only']=key_frames_only
        val['args']=args
        self[len(self)]=val
        return self

    def remove(self, function):
        self.remove(function)
