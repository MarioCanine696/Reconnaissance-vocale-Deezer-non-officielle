import speech_recognition as sr
import deezer
import requests
import webbrowser
def recherche_titre(nom):
    url = f"https://api.deezer.com/search/track?q={nom}"
    response = requests.get(url)
    data = response.json()
    return data["data"][0]

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Parlez maintenant...")
    audio = r.listen(source)
try:
    text = r.recognize_google(audio, language="fr-FR")
    url = recherche_titre(text)
    print(f"Titre : {url['title']}, Artiste : {url['artist']['name']}")
    webbrowser.open(f"{url['link']}?")
    print(f"Vous avez dit : {text}")
except sr.UnknownValueError:
    print("Impossible de comprendre.")
except sr.RequestError:
    print("Erreur de connexion à l'API.")


