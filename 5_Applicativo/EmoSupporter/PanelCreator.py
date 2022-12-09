import PySimpleGUI as SG
from PIL import Image
import EmotionalRecognition as EmoRec
import os
iconPath = './assets/images/emo-sup.png'
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def confPanel(conf_data):
    SG.theme("Purple")
    # Define the window layout
    layout = [
        [SG.Text("Impostazioni", size=(45, 1), justification="center")],
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
                default=True)],
        [SG.Listbox(webcamList(), size=(50, 3), enable_events=False, key='port')],
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
        [SG.Text('Seleziona sessione:', size=(30, 1))],
        [SG.Listbox(os.listdir("./data_log/DominantEmotions"), size=(50, 5), enable_events=False, key='session')],
        [SG.Button('Resoconto Statistico', size=(45, 2))],
        [SG.Button('Resoconto Grafico', size=(45, 2))],
        [SG.Button('Salva', size=(45, 2))],
        [SG.Button('Chiudi', size=(45, 2))]
    ]
    # Create the window and show it without the plot
    window = SG.Window("Finestra di configurazione", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if event == 'Salva':
            conf_data['cam']['face'] = values['face']
            conf_data['cam']['emotion'] = values['emotion']
            conf_data['cam']['port'] = values['port']
            conf_data['output']['popup'] = values['popup']
            conf_data['output']['voice'] = values['voice']
        if event == "Report Statistico":
            EmoRec.askStatReport(values['session'])
            print("report Statistico")
        if event == "Report Grafico":
            EmoRec.askGraphReport(values['session'])
            print("report Grafico")
        if event == "Chiudi" or event == SG.WIN_CLOSED:
            break
    window.close()


def webcamList():
    ports = []
    for port in EmoRec.availablePorts():
        ports.append("Webcam " + str(port + 1) + " disponibile per l'uso")
    return ports
