import cv2
import cv2.data

class FaceDetection:
    def __init__(self, cascade_path=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.faces = None

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return self.faces
    
    def apply(self, image):
        for (x, y, w, h) in self.faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return image

def run():
    video = cv2.VideoCapture(0)
    face_detector = FaceDetection()
    while True:
        ret, frame = video.read()
        if not ret:
            break
        face_detector.process(frame)
        frame = face_detector.apply(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    run()