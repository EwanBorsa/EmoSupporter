import pystray
from PIL import Image
import EmotionalRecognition as EmoRec
import PanelCreator as Panel

iconPath = './assets/images/emo-sup.png'

conf_data = {'cam': {'face': True, 'emotion': True, 'color': 'Purple'}, 'output': {'popup': True, 'voice': True}}


def on_clicked(icon, item):
    if str(item) == "Start":
        print("Video capturing...")
        EmoRec.startVideo(conf_data['cam'])
        icon.notify("Video capturing...")
    elif str(item) == "Settings":
        Panel.confPanel(conf_data)
    elif str(item) == "Exit":
        icon.stop()


image = Image.open(iconPath)

pyIcon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Start", on_clicked),
    pystray.MenuItem("Settings", on_clicked),
    pystray.MenuItem("Exit", on_clicked)
))

pyIcon.run()
