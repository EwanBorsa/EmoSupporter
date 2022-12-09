import pystray
from PIL import Image
import EmotionalRecognition as EmoRec
import PanelCreator as Panel

iconPath = './assets/images/emo-sup.png'
conf_data = {'cam': {'face': True, 'emotion': True, 'color': 'Purple', 'port': 0},
             'output': {'popup': True, 'voice': True},
             'user': {'name': 'utente'}}

ava_ports = EmoRec.availablePorts()


def on_clicked(icon, item):
    if str(item) == "Start":
        icon.notify("Video capturing...")
        EmoRec.startVideo(conf_data)
    elif str(item) == "Settings":
        Panel.confPanel(conf_data, ava_ports)
    elif str(item) == "Exit":
        icon.stop()


image = Image.open(iconPath)
pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Start", on_clicked),
    pystray.MenuItem("Settings", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))
pyIcon.run()

