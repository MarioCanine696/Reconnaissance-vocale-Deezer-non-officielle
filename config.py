from tkinter import * 
from tkinter.messagebox import *
import pyautogui
import time
import webbrowser
import json
from main import plein_ecran


fenetre = Tk()
fenetre.title('Configuration')

def config():
    webbrowser.open("deezer://www.deezer.com/fr/")
    showinfo('Configuration', 'Quand vous serez prêt cliquez sur Ok puis placez votre souris sur le bouton play/pause de Deezer durant environ 5 secondes.')
    plein_ecran()
    time.sleep(5)
    x, y = pyautogui.position()
    print(f"Position enregistrée : ({x}, {y})")
    config_data = {
        "play_pause_button_position": {
            "x": x,
            "y": y
        }
    }
    with open("config.json", "w") as f:
        json.dump(config_data, f, indent=4)
    showinfo('Configuration', 'Configuration terminée ! Vous pouvez fermer cette fenêtre.')

Frame = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame.pack(side=LEFT, padx=20, pady=20)
Titre = Label(Frame, text="Voici la fenêtre de configuration de l'assistant vocal Deezer")
Titre.pack()
Explication1 = Label(Frame, text="Lorsque vous cliquerez sur le bouton Lancer l'application Deezer s'ouvrira")
Explication1.pack()
lancer = Button(fenetre, text="Lancer", command=config)
lancer.pack(side=TOP, padx=10, pady=10)
bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack(side=BOTTOM, padx=10, pady=10)

fenetre.mainloop()