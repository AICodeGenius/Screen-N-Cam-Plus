import cv2
from post_process import FaceCircle,TextOverlay,Contour
from time import time
from camera_feed import CameraFeed
from ai_camera import AICamera
feed = CameraFeed(AICamera(0))
face = FaceCircle()
text = TextOverlay("FPS:30",(20,20))
prev_frame_time = time()
contour = Contour()

def calculate_fps(prev_frame_time):
    fps = int(1 / (time() - prev_frame_time))
    prev_frame_time = time()
    return fps, prev_frame_time
with feed:
    while True:
        ret,frame = feed.get()
        if not ret:
            break
        t,cnt=face.is_detected()
        if t>3 or cnt==0:
            face.process(frame)
        frame=face.apply(frame)
        fps, prev_frame_time = calculate_fps(prev_frame_time)
        text.set_text("FPS: " + str(fps))
        text.apply(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
