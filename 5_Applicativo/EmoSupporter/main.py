import pystray
from PIL import Image
import PySimpleGUI as SG
import EmotionalRecognition as EmoRec
import PanelCreator as Panel

iconPath = './assets/images/emo-sup.png'

conf_data = {'cam': {'face': True, 'emotion': True, 'color': 'Purple'}}


def on_clicked(icon, item):
    if str(item) == "Start":
        print("Video capturing...")
        EmoRec.start_video(conf_data['cam'])
        icon.notify("Video capturing...")
    elif str(item) == "Settings":
        Panel.confPanel()
    elif str(item) == "Exit":
        icon.stop()


image = Image.open(iconPath)

pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Start", on_clicked),
    pystray.MenuItem("Settings", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))

pyIcon.run()
