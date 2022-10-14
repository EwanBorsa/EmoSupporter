import pystray
from PIL import Image
# from PIL.Image import core as _imaging
import PySimpleGUI as SG
import cv2
import numpy as np

iconDir = './assets/emo-sup.png'
motion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
# Haar Cascade classifiers are an effective way for object detection.
face_classifier = cv2.CascadeClassifier()
face_classifier.load(cv2.samples.findFile("haarcascade_frontalface_default.xml"))


def conf_panel():
    SG.theme("LightGreen")

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
        [
            SG.Radio("canny", "Radio", size=(10, 1), key="-CANNY-"),
            SG.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER A-",
            ),
            SG.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(20, 15),
                key="-CANNY SLIDER B-",
            ),
        ],
        [
            SG.Radio("blur", "Radio", size=(10, 1), key="-BLUR-"),
            SG.Slider(
                (1, 11),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-BLUR SLIDER-",
            ),
        ],
        [
            SG.Radio("hue", "Radio", size=(10, 1), key="-HUE-"),
            SG.Slider(
                (0, 225),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-HUE SLIDER-",
            ),
        ],
        [
            SG.Radio("enhance", "Radio", size=(10, 1), key="-ENHANCE-"),
            SG.Slider(
                (1, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-ENHANCE SLIDER-",
            ),
        ],
    ]

    # Create the window and show it without the plot
    window = SG.Window("Configuration panel", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == SG.WIN_CLOSED:
            break
    window.close()


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
        # Print the data about the recognition of faces on the webcam
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


def on_clicked(icon, item):
    if str(item) == "Start":
        print("Video capturing...")
        start_video()
    elif str(item) == "Settings":
        conf_panel()
    elif str(item) == "Exit":
        icon.stop()


image = Image.open(iconDir)

icon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Start", on_clicked),
    pystray.MenuItem("Settings", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))

icon.run()