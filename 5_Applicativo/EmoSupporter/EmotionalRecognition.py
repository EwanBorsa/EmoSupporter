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
import random

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

model = models.Sequential()

iconPath = './assets/emo-sup.png'
haarcascadePath = './assets/haarcascade_frontalface_default.xml'
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
emotion_colors = ['Red', 'Green', 'Purple', 'Yellow', 'Blue', 'Orange', 'Gray']
#                 A  D  F  H  Sa S  N
emotion_values = [0, 0, 0, 0, 0, 0, 0]
counters = {'angry': 1, 'fear': 1, 'disgust': 1, 'sad': 1}
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(haarcascadePath))
dateToday = str(datetime.datetime.now().year) + "." + \
            str(datetime.datetime.now().month) + "." + \
            str(datetime.datetime.now().day)

full_scrn = True


# dataset1 = tf.data_log.Dataset.from_tensor_slices(tf.random.uniform([4, 10]))
# print(dataset1.element_spec)


def calculatePerc():
    tot_emotion = 1
    for value in emotion_values:
        tot_emotion += value
    emotion_perc = [0, 0, 0, 0, 0, 0, 0]
    for i in emotion_perc:
        emotion_perc[i] = emotion_values[i] / tot_emotion
    return emotion_perc


def makeStatText():
    emotion_perc = calculatePerc()
    text = "\t_\tStatistic _ Report\t_\n\n\n"
    i = 0
    for value in emotion_perc:
        text += "\n\tEmotion: " + emotion_labels[i] + " = " + str(value) + " %\n"
        i += 1
    return text


def askStatReport():
    text = makeStatText()


def makeGraph():
    print('d')
    # make a graph


def askGraphReport():
    print("d")
    # make


def makeTextLog(name, text, date):
    file = open("data_log/" + date + "_" + name, "a")
    file.write(text)


def startVideo(cam_conf):
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
        try:
            date_today = str(datetime.datetime.now().year) + "." + \
                         str(datetime.datetime.now().month) + "." + \
                         str(datetime.datetime.now().day)
            file = open("data_log/" + date_today + "_DominantEmotions", "a")
            analyze = DeepFace.analyze(frame, actions=('emotion',), enforce_detection=False)
            emotion_values[0] += analyze['emotion']['angry']
            emotion_values[1] += analyze['emotion']['disgust']
            emotion_values[2] += analyze['emotion']['fear']
            emotion_values[3] += analyze['emotion']['happy']
            emotion_values[4] += analyze['emotion']['sad']
            emotion_values[5] += analyze['emotion']['surprise']
            emotion_values[6] += analyze['emotion']['neutral']
            print(emotion_values)
            react()
            date = str(datetime.datetime.now().hour) + ":" + \
                   str(datetime.datetime.now().minute) + ":" + \
                   str(datetime.datetime.now().second)
            emotion = analyze['dominant_emotion']
            file.write(emotion + "-" + date + "\n")
        finally:
            font = cv2.FONT_HERSHEY_DUPLEX
        if cam_conf['emotion']:
            if len(faces) == 0:
                cv2.putText(img=frame,
                            text="Faccia non rilevata",
                            org=(5, 25),
                            fontFace=font,
                            fontScale=1,
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
        # Do delle impostazioni lla finestra in base alla scelta dell'utente
        # cv2.setWindowProperty(frame=frame, full_scrn=full_scrn)
        # Display the image
        if cam_conf['face']:
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


def listaPorte():
    # Controlla le porte(per la webcam) e ritorna quali ci sono funzionano
    is_working = True
    dev_port = 0
    working_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print('Port ' + str(dev_port) + ' is not working.')
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
        dev_port += 1
    return working_ports


def react():
    exp = 1000
    if emotion_values[0] > counters['angry'] * exp:
        counters['angry'] += counters['angry']
        imagePopUp('cute')
        print('angry')
    if emotion_values[1] > counters['disgust'] * exp:
        counters['disgust'] += counters['disgust']
        imagePopUp('cute')
        print('disgust')
    if emotion_values[2] > counters['fear'] * exp:
        counters['fear'] += counters['fear']
        if random.randint(0, 1) == 0:
            imagePopUp('calm')
        else:
            imagePopUp('cute')
        print('fear')
    if emotion_values[4] > counters['sad'] * 1000:
        counters['sad'] += counters['sad']
        if random.randint(0, 1) == 0:
            imagePopUp('comic')
        else:
            imagePopUp('cute')
        print('sad')


def imagePopUp(img_type):
    image_address = ''
    if img_type == 'cute':
        print('cute')
        if random.randint(0, 1) == 0:
            image_address = 'assets/images/kitties/' + str(random.randint(1, 9)) + '.jpg'
        else:
            image_address = 'assets/images/puppies/' + str(random.randint(1, 9)) + '.jpg'
    if img_type == 'comic':
        print('comic')
        image_address = 'assets/images/jokes/' + str(random.randint(1, 19)) + '.jpg'
    if img_type == 'calm':
        print('calm')
        image_address = 'assets/images/calm_places/' + str(random.randint(1, 9)) + '.jpg'
    cv2.imshow("Image", cv2.imread(image_address, 1))


# start_video()
print(listaPorte())