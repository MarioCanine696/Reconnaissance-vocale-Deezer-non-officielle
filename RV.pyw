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

# Initialisation Porcupine
with open("api_key.txt", "r", encoding="utf-8") as f:
        contenu = f.read()
porcupine = pvporcupine.create(keyword_paths=["porcupine/Et-assistant_fr_windows_v4_0_0.ppn"],model_path="porcupine/porcupine_params_fr.pv", access_key=contenu)
RATE = 16000

def play_pygame(fichier):
    try:
        pygame.mixer.init()
        pygame.mixer.init()
        pygame.mixer.music.load(fichier)
        pygame.mixer.music.play()
    except Exception as e:
        print("Erreur lecture fichier audio :",e)

def parler(texte):
    try:
        pygame.mixer.init()
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        nom = f"son/{texte}.mp3"
        tts = gTTS(texte,lang="fr")
        tts.save(nom)
        pygame.mixer.music.load(nom)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove(nom)
    except Exception as e:
        try:
            pygame.mixer.music.load(f"son/{texte}.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            os.remove(nom)
        except Exception:
            print("Erreur lecture fichier audio :",e)

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
    list_types = ["augmente","baisse","pause","lance","relance","play","arrête","stop","album","record","disque","playlist","liste","playliste","artiste","artist","auteur","chanteur","flow","flo","Flow","Flo","titre","track","chanson"]
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
    recherche_bouton(type,response)

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

def recherche_bouton(type,response):
    if type.lower() in ["flow","flo"]:
        recherche_flow()
        return
    if response is None:
        webbrowser.open("deezer://")
        return
    webbrowser.open("deezer://" + response["link"])
    if type in ["album","record","disque","playlist","liste","playliste"]:
        time.sleep(2)
        image_path = "images/playlist.png"
    elif type in ["artiste","artist","auteur","chanteur"]:
        time.sleep(2)
        image_path = "images/artiste.png"
    elif type in ["titre","track","chanson"]:
        time.sleep(5)
        image_path = "images/play.png"
    else:
        time.sleep(2)
        image_path = "images/play.png"
    start_time = time.time()
    while time.time() - start_time < 20:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen(image_path,confidence=0.8)
            if bouton:
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
                print("Bouton cliqué.")
                break
        except Exception:
            pass
        time.sleep(0.1)
    print("Bouton non trouvé après 10 secondes.")
    time.sleep(2)

def play_deezer():
    webbrowser.open("deezer://www.deezer.com/fr/")
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen("images/play_deezer.png",confidence=0.8)
            if bouton:
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
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
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
                print("Pause cliqué.")
                time.sleep(1)
                break
        except Exception:
            pass
        time.sleep(0.1)
    print("Bouton non trouvé après 10 secondes.")
    time.sleep(2)

def recherche_flow():
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen("images/flow.png",confidence=0.8)
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
        time.sleep(2)
        return None
    elif type in ["titre","track","chanson"]:
        response = recherche_titre("track",titre)
        return response
    elif type in ["album","record","disque"]:
        response = recherche_titre("album",titre)
        return response
    elif type in ["artiste","artist","auteur","chanteur"]:
        response = recherche_titre("artist",titre)
        return response
    elif type in ["playlist","liste","playliste"]:
        response = recherche_titre("playlist",titre)
        return response
    else:
        response = recherche_titre("track",titre)
        return response

def start():
    print("###########################################################")
    print(f'#     Reconnaissance vocale Deezer version {version}     #')
    print("###########################################################")
    print("Cette application n'est pas officielle et est réservée à un usage personnel")
    print("Si un problème survient, merci de contacter l'auteur.")

if __name__ == '__main__':
    start()
    print("Assistant vocal Deezer en écoute dites Hey Deezer pour lancer une commande vocale et dites Arrête Deezer pour arrêter l'assistant.")
    parler("Lancement de l'assistant vocal.")
    with sd.InputStream(
    channels=1, samplerate=RATE, blocksize=porcupine.frame_length, dtype='int16', callback=ecoute_continu):
        print("Assistant en écoute…")
        while True:
            pass