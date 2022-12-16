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
    if str(item) == "Inizia registrazione":
        icon.notify("Video capturing...")
        EmoRec.startVideo(conf_data)
    elif str(item) == "Impostazioni":
        Panel.confPanel(conf_data, ava_ports)
    elif str(item) == "Esci dall'app":
        icon.stop()


image = Image.open(iconPath)
pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Inizia registrazione", on_clicked),
    pystray.MenuItem("Impostazioni", on_clicked),
    pystray.MenuItem("Esci dall'app", on_clicked)
))
pyIcon.run()

