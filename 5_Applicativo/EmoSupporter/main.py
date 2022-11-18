import pystray
from PIL import Image
import PySimpleGUI as SG
import EmotionalRecognition as EmoRec

iconPath = './assets/images/emo-sup.png'

conf_data = {'cam': {'face': True, 'emotion': True, 'color': 'Purple'}}


def conf_panel():
    SG.theme("Purple")
    # Define the window layout
    layout = [
        [SG.Text("Settings", size=(60, 1), justification="center")],
        [
            SG.Text('Impostazioni Cam: '),
            SG.Checkbox(
                'Mostra faccia',
                key='seeFace',
                enable_events=True,
                default=True),
            SG.Checkbox(
                'Mostra emozioni',
                key='seeEmo',
                enable_events=True,
                default=True)
        ],
        [SG.Text('Reports', size=(60, 2), justification='center')],
        [SG.Button('Ask statistic report', size=(60, 2))],
        [SG.Button('Ask graphics report', size=(60, 2))]
    ]

    # Create the window and show it without the plot
    window = SG.Window("Configuration panel", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if conf_data['cam']:
            conf_data['cam']['face'] = values['seeFace']
            conf_data['cam']['emotion'] = values['seeEmo']
        if event == 'Ask statistic report':
            print('stat report')
            EmoRec.askStatReport()
        if event == 'Ask graphics report':
            print('graph report')
            EmoRec.askGraphReport()
        if event == "Exit" or event == SG.WIN_CLOSED:
            break
    window.close()


def on_clicked(icon, item):
    if str(item) == "Start":
        print("Video capturing...")
        EmoRec.start_video(conf_data['cam'])
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
