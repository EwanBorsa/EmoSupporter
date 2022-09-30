import pystray
import PIL.Image

image = PIL.Image.open("emo-sup.png")


def on_clicked(icon, item):
    if str(item) == "Say Hello":
        print("Hello World")
    elif str(item) == "Exit":
        icon.stop()

icon = pystray.Icon("EmoSupporter", image, menu=pystray.Menu(
    pystray.MenuItem("Say Hello", on_clicked),
    pystray.MenuItem("Exit", on_clicked
))

icon.run()
