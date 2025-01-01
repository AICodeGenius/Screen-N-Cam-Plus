import time
import cv2
from camera_feed import CameraFeed
import numpy as np

class PostProcess(dict):
    
    def __init__(self, camera_feed:CameraFeed):
        self.camera_feed = camera_feed
        self.__key_frame__ = None
        self.__previous_value__ = 0
        self.__last_key_frame_time__ = time.time()
    
    def key_frame_time_lapsed(self):
        if self.__last_key_frame_time__:
            if time.time() - self.__last_key_frame_time__ > 1:
                self.__last_key_frame_time__ = time.time()
                return True
            else:
                return False
        else:
            self.__last_key_frame_time__ = time.time()
            return True

    def get_frame(self):
        frame = self.camera_feed.get()
        if self.__key_frame__ is None:
            self.__key_frame__ = np.zeros(frame.shape, dtype=np.uint8)
        current_value = np.sum(frame)
        key_frame=False
        if abs(current_value - self.__previous_value__)/current_value > 0.25:
            self.__previous_value__ = current_value
            key_frame=True
        for function in self.keys():
            print(self[function])
            if self[function]['key_frame_only']:
                if key_frame:
                    print('Processing keyframe ' + self[function]['call'].__name__)
                    processed_frame=frame.copy()
                    print('processed frame share before ' + str(processed_frame.shape))
                    processed_frame = self[function]['call'](processed_frame, *self[function]['args'])
                    print('processed frame share after ' + str(processed_frame.shape))
                    self.__key_frame__ = np.subtract(frame,processed_frame)
                    frame = np.add(self.__key_frame__, frame)
                    
            else:
                print('Processing ' + self[function]['call'].__name__)
                frame = np.add(self.__key_frame__, frame)
                frame = self[function]['call'](frame, *self[function]['args'])
        return frame, key_frame
    
    def add(self, function,key_frames_only=False,args:list=[]):
        val:dict = {}
        val['call']=function
        val['key_frame_only']=key_frames_only
        val['args']=args
        self[function]=val
        return self

    def remove(self, function):
        self.remove(function)

if __name__ == "__main__":
    from ai_camera import AICamera
    import post_process_functions as ppf
    camera_feed = CameraFeed()
    cam = AICamera(0)
    cam.get_config().turn_on_metrics()
    cam.start_stream(camera_feed)
    post_process = PostProcess(camera_feed)
    post_process.add(ppf.face_detection, key_frames_only=True)
    
    while True:
        frame, key_frame = post_process.get_frame()
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.stop_stream()
    cv2.destroyAllWindows()