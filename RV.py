import speech_recognition as sr
import requests
import webbrowser
import time
import pyautogui
import sys
from nava import play
import pygetwindow as gw

version = "beta 1.0.0"

def recherche_titre(type, nom):
    try:
        url = f"https://api.deezer.com/search/{type}?q={nom}"
        response = requests.get(url)
        data = response.json()
        if data == response.json():
            print("Recherche effectuée avec succès.")
            return data["data"][0]
        else:
            print("Aucun résultat trouvé.")
            time.sleep(2)
            sys.exit(1)
    except Exception:
        print("Erreur lors de la recherche du titre.")
        time.sleep(2)
        sys.exit(1)

def recherch_bouton(image_path):
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            bouton = pyautogui.locateOnScreen(image_path, confidence=0.8)
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
            bouton = pyautogui.locateOnScreen("images/flow.png", confidence=0.8)
            if bouton:
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
                print("Flow cliqué.")
                break
        except Exception:
           pyautogui.scroll(-500) 
        time.sleep(0.1)

def plein_ecran():
    fenetre = gw.getWindowsWithTitle("Deezer")[0]
    if not fenetre.isMaximized:
        fenetre.maximize()

def reconnaissance_vocale():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play("start_enr.mp3")
        print("Parlez maintenant...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="fr-FR")
        type = text.split(" ", 1)[0]
        titre = text.split(" ", 1)[1:]
        print(f"Vous avez dit : {type} " + ' '.join(titre))
        return text
    except sr.UnknownValueError:
        print("Impossible de comprendre.")
        time.sleep(2)
    except sr.RequestError:
        print("Erreur de connexion à l'API de reconnaisance vocale.")
        time.sleep(2)
        sys.exit()

def analyse_son(son):
    type = son.split(" ", 1)[0]
    titre = son.split(" ", 1)[1:]
    if type in ["flow", "flo", "Flow", "Flo"]:
        print("Recherche du Flow...")
        time.sleep(2)
        return None
    elif type == "titre" or type == "track" or type == "chanson":
        response = recherche_titre("track", titre)
        print(f"Titre : {response['title']}, Artiste : {response['artist']['name']}")
        return response
    elif type == "album" or type == "record" or type == "disque":
        response = recherche_titre("album", titre)
        return response
    elif type == "artiste" or type == "artist" or type == "auteur" or type == "chanteur":
        response = recherche_titre("artist", titre)
        print(f"Artiste : {response['name']}")
        return response
    elif type == "playlist" or type == "liste" or type == "playliste":
        response = recherche_titre("playlist", titre)
        print(f"Playlist : {response['title']}")
        return response
    else:
        print("Type non reconnu. Veuillez dire 'Flow', 'Titre', 'Album', 'Artiste' ou 'Playlist' puis le titre.")
        time.sleep(0.2)
        print("Recherche par défaut du titre...")
        time.sleep(0.2)
        response = recherche_titre("track", titre)
        print(f"Titre : {response['title']}, Artiste : {response['artist']['name']}")
        return response

if __name__ == '__main__':
    print("###########################################################")
    print(f'#     Reconnaissance vocale Deezer version {version}     #')
    print("###########################################################")
    print("Cette application n'est pas officielle et est réservée à un usage personnel")
    print("Si un problème survient, merci de contacter l'auteur.")
    son = reconnaissance_vocale()
    response = analyse_son(son)
    if response is None:
        webbrowser.open("deezer://https://www.deezer.com/fr/")
        recherche_flow()
    else:
        type = son.split(" ", 1)[0]
        webbrowser.open(f"deezer://{response['link']}?")
        if type in ["album", "record", "disque", "playlist", "liste", "playliste"]:
            time.sleep(2)
            recherch_bouton("images/playlist.png")
        if type in ["artiste", "artist", "auteur", "chanteur"]:
            time.sleep(2)
            recherch_bouton("images/artiste.png")
        if type in ["flow", "flo", "Flow", "Flo"]:
            pass
        else:
            time.sleep(2)
            recherch_bouton("images/play.png")
