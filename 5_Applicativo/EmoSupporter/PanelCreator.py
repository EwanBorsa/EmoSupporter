import PySimpleGUI as Sg
from PIL import Image
import EmotionalRecognition as EmoRec
import os
iconPath = './assets/images/emo-sup.png'
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def conf_panel(conf_data):
    ava_ports = EmoRec.available_ports()
    Sg.theme("Purple")
    # Define the window layout
    layout = [
        [Sg.Text("Impostazioni", size=(45, 1), justification="center")],
        [Sg.Text('Nome utente: '), Sg.InputText("utente", size=(45, 1), key="name")],
        [
            Sg.Text('WebCam: '),
            Sg.Checkbox(
                'Mostra faccia',
                key='face',
                enable_events=True,
                default=True),
            Sg.Checkbox(
                'Mostra emozioni',
                key='emotion',
                enable_events=True,
                default=True)],
        [Sg.Text("Webcam disponibili per l'uso:")],
        [Sg.Combo(webcam_list(ava_ports), size=(50, 3), enable_events=False, key='port')],
        [
            Sg.Text('Output: '),
            Sg.Checkbox(
                'Mostra immagini pop-up',
                key='popup',
                enable_events=True,
                default=True),
            Sg.Checkbox(
                'Abilita audio',
                key='voice',
                enable_events=True,
                default=True)
        ],
        [Sg.Text('Seleziona sessione:', size=(30, 1))],
        [Sg.Combo(os.listdir("./data_log/DominantEmotions"), size=(50, 5), enable_events=False, key='session')],
        [Sg.Button('Resoconto Statistico', size=(45, 2), enable_events=True)],
        [Sg.Button('Resoconto Grafico', size=(45, 2), enable_events=True)],
        [Sg.Button('Salva', size=(45, 2))],
        [Sg.Button('Chiudi', size=(45, 2))]
    ]
    # Create the window and show it without the plot
    window = Sg.Window("Finestra di configurazione", layout, location=(700, 350))
    while True:
        event, values = window.read(timeout=20)
        if event == 'Salva':
            print(values)
            conf_data['cam']['face'] = values['face']
            conf_data['cam']['emotion'] = values['emotion']
            if values['port']:
                conf_data['cam']['port'] = int(values['port'])
            conf_data['output']['popup'] = values['popup']
            conf_data['output']['voice'] = values['voice']
            conf_data['user']['name'] = values['name']
        if event == "Resoconto Statistico":
            print("Inizio report Statistico")
            EmoRec.ask_stat_report(values['session'])
            print("Fine report Statistico")
        if event == "Resoconto Grafico":
            print("Inizio report Grafico")
            EmoRec.ask_graph_report(values['session'])
            print("Fine report Grafico")
        if event == "Chiudi" or event == Sg.WIN_CLOSED:
            break
    window.close()


def webcam_list(ava_ports):
    ports = []
    for port in ava_ports:
        ports.append(str(port))
    return ports


def session_list():
    emo_list = os.listdir("./data_log/DominantEmotions")
    for session in emo_list:
        print(session)

