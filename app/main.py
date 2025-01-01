import os
import cv2
from Modules import camera as cams

if os.path.exists("output") is False:
    os.mkdir("output")

cg=cams.CameraGroup()
for cam_id in cams.detect_all_cameras():
    cg.add_camera(cam_id)
if len(cg) >= 1:
    cv2.namedWindow("Multiple Cameras", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Multiple Cameras", 800, 600)
    cv2.moveWindow("Multiple Cameras", 0, 0)
    cv2.setWindowTitle("Multiple Cameras", "Multiple Cameras")
    fourcc=cv2.VideoWriter_fourcc('I','4','2','0') #*'MP42') #
    fps=30
    size = cg.capture_size()
    out=cv2.VideoWriter('output/cam.avi',fourcc,fps,size)
    
    # Capture frames from multiple cameras and display them
    while True:
        frame = cg.get_as_single_frame()
        if frame is not None:
            out.write(frame)
            cv2.imshow("Multiple Cameras", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    for camera in frames:
        camera.release()
    out.release()
    cv2.destroyAllWindows()


