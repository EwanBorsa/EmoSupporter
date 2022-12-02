import PySimpleGUI as SG
from PIL import Image
import EmotionalRecognition as EmoRec

iconPath = './assets/images/emo-sup.png'

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def confPanel(conf_data):
    SG.theme("Purple")
    # Define the window layout
    layout = [
        [SG.Text("Impostazioni", size=(60, 1), justification="center")],
        [
            SG.Text('WebCam: '),
            SG.Checkbox(
                'Mostra faccia',
                key='face',
                enable_events=True,
                default=True),
            SG.Checkbox(
                'Mostra emozioni',
                key='emotion',
                enable_events=True,
                default=True),

            SG.Listbox(EmoRec.listaPorte(),
                       size=(20, 4),
                       enable_events=False,
                       key='_LIST_'),
        ],
        [
            SG.Text('Output: '),
            SG.Checkbox(
                'Mostra immagini pop-up',
                key='popup',
                enable_events=True,
                default=True),
            SG.Checkbox(
                'Silenzia voce',
                key='voice',
                enable_events=True,
                default=True)
        ],
        [SG.Text('Richiedi:', size=(60, 2), justification='center')],
        [SG.Button('Report Statistico', size=(60, 2))],
        [SG.Button('Report Grafico', size=(60, 2))],
        [SG.Button('Salva', size=(60, 2))],
        [SG.Button('Chiudi', size=(60, 2))]
    ]
    # Create the window and show it without the plot
    window = SG.Window("Finestra di configurazione", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if event == 'Salva':
            conf_data['cam']['face'] = values['face']
            conf_data['cam']['emotion'] = values['emotion']
            conf_data['output']['popup'] = values['popup']
            conf_data['output']['voice'] = values['voice']
        if event == 'Report Statistico':
            print('Report Statistico')
            EmoRec.askStatReport()
        if event == 'Report Grafico':
            print('Report Grafico')
            EmoRec.askGraphReport()
        if event == "Chiudi" or event == SG.WIN_CLOSED:
            break
    window.close()


def reportPanel():
    SG.theme("Blue")
    # Define the window layout
    layout = [

    ]
    # Create the window and show it without the plot
    window = SG.Window("Report", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)

        if event == "Exit" or event == SG.WIN_CLOSED:
            break
    window.close()
