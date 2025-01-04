import cv2
import mss
import numpy as np
import time
import threading
from feed_provider import FeedProvider

class Screen:
    def __init__(self, monitor=1):
        self.monitor = monitor
        self.sct = mss.mss()
        self.monitor_info = self.sct.monitors[self.monitor]
        self.monitor_width = self.monitor_info["width"]
        self.monitor_height = self.monitor_info["height"]
        self.frame = None
        self.frame_time = None
        self.fps = None
        self.prev_frame_time = time.time()
        self.capture_time = None
        self.__name__ = "Screen Capture"
        self.__capture__ = None
        self.__capture_frame__ = None
    
    def start_recording(self, fps:int, feed:FeedProvider):
        self.__capture_thread__ = threading.Thread(target=self.__start_recording, args=(fps, feed))
        self.__capture_thread__.start()

    def __start_recording(self, fps:int,feed:FeedProvider):
        self.fps = fps
        self.__capture__ = True
        self.__capture_frame__ = None
        fps=0
        with self.sct:
            while self.__capture__:
                self.__capture_frame__ = self.sct.grab(self.monitor_info)
                self.frame = np.array(self.__capture_frame__)
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGRA2BGR)
                self.frame_time = time.time()
                self.capture_time = self.frame_time - self.prev_frame_time
                self.prev_frame_time = self.frame_time
                feed.put(self.frame)

    def stop_recording(self):
        self.__capture__ = False
        self.__capture_thread__.join()
        
    def is_recording(self):
        return self.__capture__
    
    def get_frame(self):
        return self.frame
    
    def get_frame_time(self):
        return self.frame_time
    
    def get_fps(self):
        return self.fps
    
    
if __name__ == "__main__":
    from post_process import TextOverlay
    text = TextOverlay("FPS:30",(20,20))
    screen = Screen(1)
    feed = FeedProvider()
    screen.start_recording(144,feed)
    last_time=time.time()
    fps=0
    while True:
        frame = feed.get()
        if frame is None:
            continue
        fps+=1
        frame=text.apply(frame)
        #reset fps if last_time is more than 1 sec
        if time.time()-last_time>1:
            last_time=time.time()
            text.set_text("FPS: " + '{:3d}'.format(fps))
            fps=0
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    screen.stop_recording()
