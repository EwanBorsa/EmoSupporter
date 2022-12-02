import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def calculatePerc(emotion_values):
    tot_emotion = 1
    for value in emotion_values:
        tot_emotion += value
    emotion_perc = [0, 0, 0, 0, 0, 0, 0]
    for i in emotion_perc:
        emotion_perc[i] = emotion_values[i] / tot_emotion
    return emotion_perc


def makeStatText(emotion_values):
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