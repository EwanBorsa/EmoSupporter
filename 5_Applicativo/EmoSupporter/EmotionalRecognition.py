# from xml.etree.ElementTree import TreeBuilder
import cv2
from deepface import DeepFace
from keras import models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# import tensorflow as tf
import os
import datetime

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

model = models.Sequential()

iconPath = './assets/emo-sup.png'
haarcascadePath = './assets/haarcascade_frontalface_default.xml'
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emotion_colors = ['Red', 'Green', 'Purple', 'Yellow', 'Blue', 'Orange',  'Gray']
#                 A  D  F  H  S  S  N
emotion_values = [0, 0, 0, 0, 0, 0, 0]
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(haarcascadePath))
dateToday = str(datetime.datetime.now().year) + "." + \
            str(datetime.datetime.now().month) + "." + \
            str(datetime.datetime.now().day)


# dataset1 = tf.data_log.Dataset.from_tensor_slices(tf.random.uniform([4, 10]))
# print(dataset1.element_spec)

def start_video():
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
        # Print the data_log about the recognition of faces on the webcam
        # print(faces)  # DEBUG
        # making a try and except condition in case of any errors
        emotion = "null"
        try:
            date_today = str(datetime.datetime.now().year) + "." + \
                         str(datetime.datetime.now().month) + "." + \
                         str(datetime.datetime.now().day)
            file = open("data_log/" + date_today + "_DominantEmotions", "a")
            file = open("data_log/" + date_today + "_DominantEmotions", "a")
            analyze = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            print(analyze)
            emotion_values[0] += analyze['emotion']['angry']
            emotion_values[1] += analyze['emotion']['disgust']
            emotion_values[2] += analyze['emotion']['fear']
            emotion_values[3] += analyze['emotion']['happy']
            emotion_values[4] += analyze['emotion']['sad']
            emotion_values[5] += analyze['emotion']['surprise']
            emotion_values[6] += analyze['emotion']['neutral']
            print(emotion_values)
            #  print(analyze)  # DEBUG
            date = str(datetime.datetime.now().hour) + ":" + \
                   str(datetime.datetime.now().minute) + ":" + \
                   str(datetime.datetime.now().second)
            emotion = analyze['dominant_emotion']
            file.write(emotion + "-" + date + "\n")
        finally:
            font = cv2.FONT_HERSHEY_DUPLEX
        # for face in faces:  # For all faces
        if len(faces) == 0:
            cv2.putText(img=frame,
                        text="Undetected face",
                        org=(5, 5),
                        fontFace=font,
                        fontScale=0.5,
                        color=(111, 111, 111))
        else:
            face = faces[0]  # For one face
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
    # Close the file that im writing
    file.close()
    # Close all active windows
    cv2.destroyAllWindows()


ImageAddress = 'assets/images/jokes/1.jpg'
ImageItself = Image.open(ImageAddress)
cv2.imshow(ImageItself)
cv2.draw()
cv2.pause(10)  # pause how many seconds
cv2.close()
start_video()