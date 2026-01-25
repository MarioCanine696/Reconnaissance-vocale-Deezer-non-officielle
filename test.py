from rv import plein_ecran
import webbrowser
import time
import pyautogui

def play_deezer():
    webbrowser.open("deezer://www.deezer.com/fr/")
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            plein_ecran()
            print("Recherche du bouton Play...")
            mole = pyautogui.locateCenterOnScreen(
            'images/image.png',
            grayscale=True,
            confidence=0.8
            )
            if mole:
                pyautogui.click(mole.x, mole.y)
                print("Play cliqué.")
                time.sleep(1)
                break
        except Exception:
            pass
        time.sleep(0.1)
    print("Bouton non trouvé après 10 secondes.")
    time.sleep(2)

play_deezer()