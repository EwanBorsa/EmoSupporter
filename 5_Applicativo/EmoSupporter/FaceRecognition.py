import pystray
from PIL import Image
# from PIL.Image import core as _imaging
import PySimpleGUI as SG
import cv2
import numpy

iconPath = './assets/emo-sup.png'
haarcascadePath = './assets/haarcascade_frontalface_default.xml'
motion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(haarcascadePath))


def start_video():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    # scaling factor
    scaling_factor = 2
    # Loop until you hit the Esc key
    while True:
        # Capture the current frame
        ret, frame = cap.read()
        # Create a gray version of the frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces on the webcam
        faces = face_classifier.detectMultiScale(frame_gray)
        # Print the data_log about the recognition of faces on the webcam
        for face in faces:
            x, y, w, h = face
            new_frame = cv2.rectangle(frame, (x, y), (x+w, y+h), color=(219, 112, 147), thickness=3)
        # Resize the normal frame
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        # Display the image
        cv2.imshow('Emotion Detector', new_frame)
        # Detect if the Esc key has been pressed
        if cv2.waitKey(1) == 27:
            break
    # Release the video capture object
    cap.release()
    # Close all active windows
    cv2.destroyAllWindows()