# Subtitles by AI - Application Web de Margot Berton

Dernière mise à jour : 27/07/2023
Objectif : générer automatiquement des sous-titres (IA) pour une vidéo située localement sur l'ordinateur


## Exécuter l'application

* Il est nécessaire d'avoir les dépendances requises, définies dans requirements.txt, notamment :
	- django
	- django-bootstrap5
* Se positionner dans code, et taper la commande : python manage.py runserver
* Aller à l'URL home/


## Choix du modèle ASR

Différents outils d'ASR ont étés testés, à savoir :
	- Google Web Speech
	- Google Cloud Speech
Le code a approfondi l'utilisation de Google Cloud Speech. Si toutefois l'utilisateur souhaite utiliser un autre mode, il faut changer la variable asr_function dans le fichier ./subtitlingAI/ML/data_process.py.


## A faire côté Django
* Déployer une VM
* Choisir le répertoire de téléchargement du SRT
* Améliorer HTML/CSS
* Messages flash pour indiquer processing et fichier généré/sauvegardé

## A faire côté Data process
* Gérer automatiquement erreurs liés à Google Storage (il faut vider le bucket)

* Commenter tout le code
* Gérer accès au projet (si trop d'utilisateurs utilisent mon projet -> surcoût Google Cloud, mêmes noms de vidéos uploadées en même temps ?)
* Rapport FR et EN (à faire relire par papa)
* Réfléchir à mon propre modèle ?
