from xml.etree.ElementTree import TreeBuilder
import cv2
from deepface import DeepFace
from keras import models
import numpy as np
# import tensorflow as tf
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

model = models.Sequential()

iconPath = './assets/emo-sup.png'
haarcascadePath = './assets/haarcascade_frontalface_default.xml'
motion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(haarcascadePath))

# dataset1 = tf.data.Dataset.from_tensor_slices(tf.random.uniform([4, 10]))
# print(dataset1.element_spec)

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
    # making a try and except condition in case of any errors
    emotion = "null"
    try:
        analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        print(analyze)  # DEBUG
        emotion = analyze['dominant_emotion']
    finally:
        font = cv2.FONT_HERSHEY_DUPLEX
    for face in faces:
        x, y, w, h = face
        cv2.putText(img=frame,
                    text=emotion,
                    org=(x, y),
                    fontFace=font,
                    fontScale=1,
                    color=(250, 130, 169))
        cv2.rectangle(frame,
                      (x, y),
                      (x + w, y + h),
                      color=(200, 90, 130),
                      thickness=2)
    # Resize the normal frame
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    # Display the image
    cv2.imshow('Emotion Detector', frame)
    # Detect if the Esc key has been pressed
    if cv2.waitKey(1) == 27:
        break
# Release the video capture object
cap.release()
# Close all active windows
cv2.destroyAllWindows()
