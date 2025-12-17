import speech_recognition as sr
import requests
import webbrowser
import time
import pyautogui
import sys
def recherche_titre(nom):
    try:
        url = f"https://api.deezer.com/search/track?q={nom}"
        response = requests.get(url)
        data = response.json()
        return data["data"][0]
    except Exception:
        print("Erreur lors de la recherche du titre.")
        sys.exit(1)

def recherch_bouton(image_path): 
    try:
        bouton = pyautogui.locateOnScreen(image_path, confidence=0.8)
        pyautogui.click(bouton.left + bouton.width // 2, bouton.top + bouton.height // 2)
        return bouton
    except pyautogui.ImageNotFoundException:
        essais =+ 1
        if essais > 10:
            time.sleep(1)
            print("Bouton non trouvé.")
            sys.exit(1)
        time.sleep(0.1)
        recherch_bouton(image_path)
    
if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="fr-FR")
        print(f"Vous avez dit : {text}")
        if text == "Flow":
            print("Fonction en dévellopement")
        else:
            url = recherche_titre(text)
            print(f"Titre : {url['title']}, Artiste : {url['artist']['name']}")
            webbrowser.open(f"deezer://{url['link']}?")
            recherch_bouton("play.png")
                
    except sr.UnknownValueError:
        print("Impossible de comprendre.")
    except sr.RequestError:
        print("Erreur de connexion à l'API.")