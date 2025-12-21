import speech_recognition as sr
import requests
import webbrowser
import time
import pyautogui
import sys
import keyboard
from nava import play
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
            sys.exit()
    except Exception:
        print("Erreur lors de la recherche du titre.")
        time.sleep(2)
        sys.exit()

def recherch_bouton(image_path):
    start_time = time.time()
    while time.time() - start_time < 5:
        try:
            bouton = pyautogui.locateOnScreen(image_path, confidence=0.8)
            if bouton:
                pyautogui.click(bouton.left + bouton.width // 2,bouton.top + bouton.height // 2)
                print("Bouton cliqué.")
        except pyautogui.ImageNotFoundException:
            plein_ecran()
        time.sleep(0.1)
    print("Bouton non trouvé après 5 secondes.")
    time.sleep(2)

def plein_ecran():
    keyboard.press_and_release('f11')

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
        print("Erreur de connexion à l'API de reconnaisance vocale google.")
        time.sleep(2)
        sys.exit()

if __name__ == '__main__':
    text = reconnaissance_vocale()
    type = text.split(" ", 1)[0]
    titre = text.split(" ", 1)[1:]
    if type == "Flow":
        print("Fonction en dévellopement")
    elif type == "titre" or type == "track" or type == "chanson":
        response = recherche_titre("track", titre)
        print(f"Titre : {response['title']}, Artiste : {response['artist']['name']}")
        webbrowser.open(f"deezer://{response['link']}?")
        time.sleep(1)
        recherch_bouton("images/play.png")
    elif type == "album":
        response = recherche_titre("album", titre)
        print(f"Album : {response['title']}, Artiste : {response['artist']['name']}")
        webbrowser.open(f"deezer://{response['link']}?")
        time.sleep(1)
        recherch_bouton("images/playlist.png")
    elif type == "artiste":
        response = recherche_titre("artist", titre)
        print(f"Artiste : {response['name']}")
        webbrowser.open(f"deezer://{response['link']}?")
        time.sleep(1)
        recherch_bouton("images/artiste.png")
    elif type == "playlist":
        response = recherche_titre("playlist", titre)
        print(f"Playlist : {response['title']}")
        webbrowser.open(f"deezer://{response['link']}?")
        time.sleep(1)
        recherch_bouton("images/playlist.png")
    else:
        print("Type non reconnu. Veuillez dire 'Flow', 'Titre', 'Album', 'Artiste' ou 'Playlist' puis le titre.")
        time.sleep(5)
        sys.exit()
