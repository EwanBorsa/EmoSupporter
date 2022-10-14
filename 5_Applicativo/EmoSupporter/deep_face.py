from deepface import DeepFace
import pystray
from PIL import Image
# from PIL.Image import core as _imaging
import PySimpleGUI as SG
import cv2
import numpy as np
from xml.etree.ElementTree import TreeBuilder
import tensorflow as tf
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

iconDir = './assets/emo-sup.png'
motion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# dataset1 = tf.data.Dataset.from_tensor_slices(tf.random.uniform([4, 10]))
# print(dataset1.element_spec)


# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile("haarcascade_frontalface_default.xml"))
# Initialize video capture
cap = cv2.VideoCapture(0)
# scaling factor
scaling_factor = 1.5
# Loop until you hit the Esc key
while True:
    # Capture the current frame
    ret, frame = cap.read()
    # Create a gray version of the frame
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces on the webcam
    faces = face_classifier.detectMultiScale(frame_gray)
    # Print the data about the recognition of faces on the webcam
    # print(faces)  # DEBUG
    response = DeepFace.analyze(frame, acions=("emotions",), enforce_detection=False)
    print(response)
    for face in faces:
        x, y, w, h = face
        new_frame = cv2.rectangle(frame, (x, y), (x+w, y+h), color=(219, 112, 147), thickness=2)
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

