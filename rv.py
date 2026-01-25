from pywinauto import Application
import sys
import speech_recognition as sr
import requests
import webbrowser
import time
import pyautogui
import pygetwindow as gw
from gtts import gTTS
import pygame
import os
import pvporcupine
import sounddevice as sd
import numpy as np

version = "beta 4.1.5"

# Sécurité Porcupine
is_listening = True

# Initialisation Pygame
pygame.mixer.init()

# Initialisation Porcupine
with open("api_key.txt", "r", encoding="utf-8") as f:
        contenu = f.read()
porcupine = pvporcupine.create(keyword_paths=["porcupine/Et-assistant_fr_windows_v4_0_0.ppn"],model_path="porcupine/porcupine_params_fr.pv", access_key=contenu)
RATE = 16000

pygame.mixer.init()

def play_pygame(chemin_fichier):
    try:
        pygame.mixer.music.load(chemin_fichier)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Erreur play : {e}")

def parler(texte):
    nom_temp = "voix_temp.mp3"
    try:
        tts = gTTS(text=texte, lang='fr')
        tts.save(nom_temp)
        play_pygame(nom_temp)
        if os.path.exists(nom_temp):
            os.remove(nom_temp)
    except Exception as e:
        print(f"Erreur parler : {e}")


def volume_up():
    os.system("augmenter_volume.bat")
def volume_down():
    os.system("reduire_volume.bat")

def ecoute_continu(indata, frames, time, status):
    global is_listening
    if not is_listening:
        return
    pcm = np.frombuffer(indata, dtype=np.int16)
    result = porcupine.process(pcm)
    if result >= 0:
        print("Hotword détecté !")
        is_listening = False
        try:
            reconnaissance_vocale()
        finally:
            is_listening = True


def reconnaissance_vocale():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play_pygame("start_enr.mp3")
        print("Parlez maintenant...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="fr-FR")
        print("Tu as dit :", text)
        analyse_son(text)
    except sr.UnknownValueError:
        print("Impossible de comprendre")
        parler("Désolé, je n'ai pas compris.")
    except sr.RequestError as e:
        print("Erreur de service; {0}".format(e))
        parler("Désolé, le service de reconnaissance vocale est indisponible.")

def analyse_son(son):
    list_types = ["augmente","baisse","pause","lance","relance","playlist","arrête","stop","album","record","disque","play","liste","playliste","artiste","artist","auteur","chanteur","flow","flo","Flow","Flo","titre","track","chanson"]
    son = son.lower()
    try:
        type = next((item for item in list_types if item.lower() in son),None)
        print("Type détecté :",type)
        if type is None:
            type = "titre"
            position_type = 0
            titre = son.strip()
        elif type.lower() in ["augmente"]:
            volume_up()
            return
        elif type.lower() in ["baisse"]:
            volume_down()
            return
        elif type.lower() in ["pause"]:
            pause_deezer()
            return
        elif type.lower() in ["lance","relance","joue"]:
            play_deezer()
            return
        elif type.lower() in ["arrête","stop"]:
            print("Arrêt de l'assistant vocal Deezer.")
            parler("Arrêt de l'assistant vocal Deezer.")
            time.sleep(2)
            sys.exit()
        elif type.lower() in ["flow","flo","Flow","Flo"]:
            recherche_flow()
        else:
            position_type = son.index(type.lower())
            titre = son[position_type + len(type):].strip()
    except Exception:
        print("Aucun type détecté dans la commande vocale.")
        return
    print(f'Analyse du son : {titre}')
    response = analyse_type(type,titre)
    if response is None:
        print("Aucun résultat trouvé pour la recherche.")
        parler("Désolé, aucun résultat trouvé pour votre recherche.")
        return
    else:
        webbrowser.open("deezer://" + response['link'])
        recherche_bouton(type)

def recherche_titre(type,nom):
    try:
        url = f"https://api.deezer.com/search/{type}?q={nom}"
        response = requests.get(url)
        data = response.json()
        if data.get("data"):
            print("Recherche effectuée avec succès.")
            return data["data"][0]
        else:
            print("Aucun résultat trouvé.")
            return None
    except Exception:
        print("Erreur lors de la recherche du titre.")
        return None

def recherche_bouton(type):
    if type.lower() in ["flow","flo"]:
        recherche_flow()
        return
    app_deezer = Application(backend="uia").connect(title="Deezer")
    DEEZER_WIN = app_deezer.top_window()
    start_time = time.time()
    clicked = False
    while (time.time() - start_time < 20) and not clicked:
        try:
            plein_ecran()
            btn = DEEZER_WIN.child_window(title="Écouter", control_type="Button", found_index=0)
            btn.click_input()
            clicked = True
        except Exception as e:
            print("Erreur clic Écouter :", e)
        time.sleep(0.1)
    
    if not clicked:
        print("Bouton non trouvé après 20 secondes.")

def play_deezer():
    webbrowser.open("deezer://www.deezer.com/fr/")
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen("images/play_deezer.png",confidence=0.8)
            if bouton:
                pyautogui.click(pyautogui.center(bouton))
                print("Play cliqué.")
                time.sleep(1)
                break
        except Exception:
            pass
        time.sleep(0.1)
    print("Bouton non trouvé après 10 secondes.")
    time.sleep(2)

def pause_deezer():
    webbrowser.open("deezer://www.deezer.com/fr/")
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen("images/pause_deezer.png",confidence=0.8)
            if bouton:
                pyautogui.click(pyautogui.center(bouton))
                print("Pause cliqué.")
                time.sleep(1)
                break
        except Exception:
            pass
        time.sleep(0.1)
    print("Bouton non trouvé après 10 secondes.")

def recherche_flow():
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen("images/flow.png",confidence=0.5)
            if bouton:
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
                print("Flow cliqué.")
                break
        except Exception:
            pyautogui.scroll(-500)
        time.sleep(0.1)

def plein_ecran():
    fenetres = gw.getWindowsWithTitle("Deezer")
    if fenetres:
        if not fenetres[0].isMaximized:
            fenetres[0].maximize()


def analyse_type(type,titre):
    if type.lower() in ["flow","flo"]:
        print("Recherche du Flow...")
        return None
    elif type in ["titre","track","chanson"]:
        response = recherche_titre("track",titre)
    elif type in ["album","record","disque"]:
        response = recherche_titre("album",titre)
    elif type in ["artiste","artist","auteur","chanteur"]:
        response = recherche_titre("artist",titre)
    elif type in ["playlist","liste","playliste"]:
        response = recherche_titre("playlist",titre)
    else:
        response = recherche_titre("track",titre)
    print("Analyse type réussite.")
    return response


def start():
    print("###########################################################")
    print(f'#     Reconnaissance vocale Deezer version {version}     #')
    print("###########################################################")
    print("Cette application n'est pas officielle et est réservée à un usage personnel")
    print("Si un problème survient, merci de contacter l'auteur.")
    webbrowser.open("deezer://www.deezer.com/fr/")

if __name__ == '__main__':
    start()
    print("Assistant vocal Deezer en écoute dites Hey Deezer pour lancer une commande vocale et dites Arrête Deezer pour arrêter l'assistant.")
    parler("Lancement de l'assistant vocal.")
    with sd.InputStream(
    channels=1, samplerate=RATE, blocksize=porcupine.frame_length, dtype='int16', callback=ecoute_continu):
        print("Assistant en écoute…")
        while True:
            pass