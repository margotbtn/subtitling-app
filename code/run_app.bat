@echo off

rem Remplacez "chemin_vers_python" par le chemin complet vers l'exécutable Python (par exemple, C:\Python39\python.exe)
rem Remplacez "chemin_vers_manage_py" par le chemin complet vers manage.py

set "chemin_vers_python=chemin_vers_python"
set "chemin_vers_manage_py=chemin_vers_manage_py"

rem Exécution de l'application Django
start "" "%chemin_vers_python%" "%chemin_vers_manage_py%" runserver

rem Temporisation pour attendre que le serveur se lance complètement (ajustez le délai si nécessaire)
timeout /t 5

rem Ouvrir l'URL dans le navigateur par défaut
start "" http://127.0.0.1:8000/home/

rem Attendre jusqu'à ce que l'utilisateur ferme le navigateur pour terminer le serveur Django
:wait_loop
tasklist | find /i "python.exe" > nul
if %errorlevel% equ 0 (
    timeout /t 5
    goto wait_loop
)

echo Serveur Django arrêté.