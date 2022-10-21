import pystray
from PIL import Image
# from PIL.Image import core as _imaging
import PySimpleGUI as SG
import cv2
import EmotionalRecognition as EmoRec

# import numpy

iconPath = './assets/emo-sup.png'
haarcascadePath = './assets/haarcascade_frontalface_default.xml'
motion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile(haarcascadePath))


def conf_panel():
    SG.theme("Purple")

    # Define the window layout
    layout = [
        [SG.Text("Settings", size=(60, 1), justification="center")],
        [SG.Radio("None", "Radio", True, size=(10, 1))],
        [
            SG.Radio("threshold", "Radio", size=(10, 1), key="-THRESH-"),
            SG.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER-",
            ),
        ],
        [SG.Text("________________________", size=(60, 2), justification="center")],
        [SG.Text("Reports", size=(60, 2), justification="center")],
        [SG.Button("Ask statistic report", size=(60, 2))],
        [SG.Button("Ask graphics report", size=(60, 2))]
    ]

    # Create the window and show it without the plot
    window = SG.Window("Configuration panel", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == SG.WIN_CLOSED:
            break
    window.close()


def on_clicked(icon, item):
    if str(item) == "Start":
        print("Video capturing...")
        EmoRec.start_video()
    elif str(item) == "Settings":
        conf_panel()
    elif str(item) == "Exit":
        icon.stop()


image = Image.open(iconPath)

pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Start", on_clicked),
    pystray.MenuItem("Settings", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))

pyIcon.run()
