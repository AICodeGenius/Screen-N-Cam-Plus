from typing import Sequence
import cv2
import numpy as np
import cv2.data

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')
# hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'hand.xml')


#different types of post processing functions
def none(img):
    return img

def blur(img,size=(5,5)):
    img = cv2.GaussianBlur(img, size, 0)
    return img

def sharpen(img):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    return img

def grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    return img

def edge_detection(img):
    img = cv2.Canny(img, 100, 200)
    return img

def invert(img):
    img = cv2.bitwise_not(img)
    return img

def threshold(img):
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img

def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    return img

# face detection, copy original to resized image of longest side to 160px and smallest side to 120px.
# after receiving detectMultiScale result mark resized bigger rectangle in original image.


        
def face_detection(img, scale_factor=1.1, min_neighbors=5, min_size=(30, 30), max_size=(100, 100)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scale_factor, min_neighbors, minSize=min_size, maxSize=max_size)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img

# Hand gesture detection
def hand_gesture_detection(img):
    hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'hand.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
    for (x, y, w, h) in hands:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img
