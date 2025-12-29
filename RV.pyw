import speech_recognition as sr
import requests
import webbrowser
import time
import pyautogui
import sys
import pygetwindow as gw
from gtts import gTTS
import pygame

def play(fichier):
    pygame.mixer.init()
    pygame.mixer.music.load(fichier)
    pygame.mixer.music.play()

def parler(texte):
    tts = gTTS(texte, lang="fr")
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()


version = "beta 2.0.0"
list_types = ["album","record","disque","playlist","liste","playliste","artiste","artist","auteur","chanteur","flow","flo","Flow","Flo","titre","track","chanson"]

def ecoute_continu():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Assistant vocal Deezer en écoute dites Hey Deezer pour lancer une commande vocale et dites Arrête Deezer pour arrêter l'assistant.")
        parler("Lancement de l'assistant vocal.")
        while True:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio,language="fr-FR").lower()
                if "hey deezer" in text or "et deezer" in text:
                    time.sleep(1)
                    break
                elif "stop deezer" in text or "arrête deezer" in text:
                    print("Arrêt de l'assistant vocal Deezer.")
                    parler("Arrêt de l'assistant vocal Deezer.")
                    sys.exit(0)
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue
    son = reconnaissance_vocale()
    if not son:
        return
    son = son.lower()
    try:
        type = next((item for item in list_types if item.lower() in son),None)
        print("Type détecté :",type)
        if type is None:
            type = "titre"
            position_type = 0
        else:
            position_type = son.index(type.lower())
        titre = son[position_type + len(type):].strip()
    except Exception:
        print("Aucun type détecté dans la commande vocale.")
        return
    print(f'Analyse du son : {titre}')
    response = analyse_type(type,titre)
    recherche_bouton(type,response)
    time.sleep(2)
    print("Relance la commande vocale...")

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
        webbrowser.open("deezer://www.deezer.com/fr/")
        return
    webbrowser.open("deezer://" + response["link"])
    if type in ["album","record","disque","playlist","liste","playliste"]:
        time.sleep(2)
        image_path = "images/playlist.png"
    elif type in ["artiste","artist","auteur","chanteur"]:
        time.sleep(2)
        image_path = "images/artiste.png"
    else:
        time.sleep(2)
        image_path = "images/play.png"
    start_time = time.time()
    while time.time() - start_time < 10:
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

def reconnaissance_vocale():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play("start_enr.mp3")
        print("Parlez maintenant...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="fr-FR")
        print(f'Vous avez dit : {text}')
        return text
    except sr.UnknownValueError:
        print("Impossible de comprendre.")
        return ""
    except sr.RequestError:
        print("Erreur de connexion à l'API de reconnaisance vocale.")
        return ""

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
    while True:
        ecoute_continu()