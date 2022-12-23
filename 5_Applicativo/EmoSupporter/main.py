import pystray
from PIL import Image
import EmotionalRecognition as EmoRec
import PanelCreator as Panel

iconPath = './assets/images/emo-sup.png'
conf_data = {'cam': {'face': True, 'emotion': True, 'color': 'Purple', 'port': 0},
             'output': {'popup': True, 'voice': True},
             'user': {'name': 'utente'}}


def on_clicked(icon, item):
    if str(item) == "Inizia registrazione":
        icon.notify("Video capturing...")
        EmoRec.start_video(conf_data)
    elif str(item) == "Impostazioni":
        Panel.conf_panel(conf_data)
    elif str(item) == "Esci dall'app":
        icon.stop()


image = Image.open(iconPath)
pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Inizia registrazione", on_clicked),
    pystray.MenuItem("Impostazioni", on_clicked),
    pystray.MenuItem("Esci dall'app", on_clicked)
))
pyIcon.run()

