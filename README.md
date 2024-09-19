MiniBlog
--------

MiniBlog est un site où des utilisateurs peuvent créer un compte et poster des articles.

Le projet utilise les technologies suivantes :
### Front-end : 
- Langage : HTML5, CSS3
- Librairie : Bootstrap

### Back-end : 
- Flask

### Base de données :
- sqlite


# Installation
Dépendance : python 3.12.3, pip 24.0

Commande console sous windows

 1. Cloner le repertoire [https://github.com/gaellerem/Bloc3](https://github.com/gaellerem/Bloc3)
 2. Créer un environnement virtuel
    ``` console
    python -m venv env
    env\Scripts\activate
    ```
 4. Installer les librairies et initialiser les variables du projet
    ``` console
    pip install -r requirements.txt
    set FLASK_APP=app
    set FLASK_ENV=development
    ```
6. Lancer l'application :
    ``` console
    flask run
    ```
