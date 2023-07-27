#!/usr/bin/env python

import os
import subprocess
import webbrowser
import time

if __name__ == "__main__":
    current_path = os.path.abspath(os.path.dirname(__file__))

    #Lancement du serveur Django en arrière-plan
    django_process = subprocess.Popen(f"python {current_path}/manage.py runserver", shell=True)

    #Attendre que le serveur soit lancé
    time.sleep(5)
    
    #Ouvrir l'application dans le navigateur Web
    base_url = "http://127.0.0.1:8000"
    page_url = f"{base_url}/home/"
    webbrowser.open(page_url)
    
    try:
        django_process.wait()
    except KeyboardInterrupt:
        django_process.terminate()