# from xml.etree.ElementTree import TreeBuilder
import cv2
from deepface import DeepFace
from keras import models
import numpy as np
import matplotlib.pyplot as plt
# import tensorflow as tf
import os
import datetime
import random
import pyttsx3

engine = pyttsx3.init()
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


def askStatReport(session):
    text = makeStatText()
    print(text)


def makeGraph():
    print('d')
    # make a graph


def askGraphReport(session):
    print("d")
    # make


def makeTextLog(dir_name, text, date):
    file = open("data_log/" + dir_name + "/" + date, "a")
    file.write(text)
    file.close()


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
            analyze = DeepFace.analyze(frame, actions=('emotion',), enforce_detection=False)
            emotion_values[0] += analyze['emotion']['angry']
            emotion_values[1] += analyze['emotion']['disgust']
            emotion_values[2] += analyze['emotion']['fear']
            emotion_values[3] += analyze['emotion']['happy']
            emotion_values[4] += analyze['emotion']['sad']
            emotion_values[5] += analyze['emotion']['surprise']
            emotion_values[6] += analyze['emotion']['neutral']
            emotion = analyze['dominant_emotion']
            react()
            makeTextLog('DominantEmotions', emotion + "-" + timeNow() + "\n", dateToday())
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
                face = faces[0]  # Prendo la prima faccia
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
        # Corregge la grandezza del frame in base alla finestra
        frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        # Mostro la visione della WebCam in base alle impostazioni scelte dall'utente
        if cam_conf['face']:
            cv2.imshow('Emotion Detector', frame)
        # Se viene premuto il tasto Esc finisce il ciclo while
        if cv2.waitKey(1) == 27:
            break
    # Ferma la registrazione della Webcam
    cap.release()
    # Chiude tutte le finestre aperte
    cv2.destroyAllWindows()


def availablePorts():
    # Controlla le porte(per la webcam) e ritorna quali ci sono e quali funzionano
    is_working = True
    dev_port = 0
    working_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            # print('Port ' + str(dev_port) + ' is not working.')
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                # print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
                working_ports.append(dev_port)
        dev_port += 1
    return working_ports


def react():
    print(emotion_values)
    exp = 5000
    if emotion_values[0] > counters['angry'] * exp:
        print('angry' + str(counters['angry']))
        counters['angry'] += counters['angry']
        imagePopUp('cute')
    if emotion_values[1] > counters['disgust'] * exp:
        print('disgust' + str(counters['disgust']))
        counters['disgust'] += counters['disgust']
        imagePopUp('cute')
    if emotion_values[2] > counters['fear'] * exp:
        print('fear' + str(counters['fear']))
        counters['fear'] += counters['fear']
        if random.randint(0, 1) == 0:
            imagePopUp('calm')
        else:
            imagePopUp('cute')
    if emotion_values[4] > counters['sad'] * exp:
        print('sad' + str(counters['sad']))
        counters['sad'] += counters['sad']
        if random.randint(0, 1) == 0:
            imagePopUp('comic')
        else:
            imagePopUp('cute')


def timeNow():
    return str(datetime.datetime.now().hour) + ":" + \
           str(datetime.datetime.now().minute) + ":" + \
           str(datetime.datetime.now().second)


def dateToday():
    return str(datetime.datetime.now().year) + "." + \
           str(datetime.datetime.now().month) + "." + \
           str(datetime.datetime.now().day)


def imagePopUp(img_type):
    image_address = ''
    if img_type == 'cute':
        if random.randint(0, 1) == 0:
            image_address = 'assets/images/kitties/' + str(random.randint(1, 9)) + '.jpg'
            engine.say("Guarda questo gattino quanto è carino!")
        else:
            image_address = 'assets/images/puppies/' + str(random.randint(1, 9)) + '.jpg'
            engine.say("Guarda questo cucciolo quanto è carino!")
    if img_type == 'comic':
        image_address = 'assets/images/jokes/' + str(random.randint(1, 19)) + '.jpg'
    if img_type == 'calm':
        image_address = 'assets/images/calm_places/' + str(random.randint(1, 9)) + '.jpg'
    win_name = "Image: " + img_type
    cv2.namedWindow(win_name)
    cv2.moveWindow(win_name, random.randint(50, 100), random.randint(50, 100))
    cv2.imshow(win_name, cv2.imread(image_address, 1))


# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))


change_voice(engine, "it_IT", "VoiceGenderFemale")
# start_video()
# print(listaPorte())
