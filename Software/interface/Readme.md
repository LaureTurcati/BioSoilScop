# Interface pour Communiquer avec un CamTrap (Bookworm)

 <!-- introduire CamTrap 
___ -->
## Table des Matières
- [Interface pour Communiquer avec un CamTrap (Bookworm)](#interface-pour-communiquer-avec-un-camtrap-bookworm)
  - [Table des Matières](#table-des-matières)
  - [Introduction](#introduction)
  - [Prérequis](#prérequis)
  - [Installation](#installation)
      - [Étape 1 : Installation de Flask](#étape-1--installation-de-flask)
      - [Étape 2 : Construire l'Arborescence de Fichiers](#étape-2--construire-larborescence-de-fichiers)
      - [Étape 3 : Déploiement de l'Interface](#étape-3--déploiement-de-linterface)
  - [Détails Techniques](#détails-techniques)
      - [Fonctionnement de `server.py` et des Pages HTML](#fonctionnement-de-serverpy-et-des-pages-html)
      - [Utilisation du Map Picker (en mode WiFi)](#utilisation-du-map-picker-en-mode-wifi)
  - [Utilisation](#utilisation)
    - [Mode de Fonctionnement du CamTrap](#mode-de-fonctionnement-du-camtrap)
    - [Navigation de Fichiers avec FileBrowser](#navigation-de-fichiers-avec-filebrowser)
        - [Modification des droits](#modification-des-droits)
  - [Configuration de la mise en route du serveur et du script pour les boutons au démarage du CamTrap](#configuration-de-la-mise-en-route-du-serveur-et-du-script-pour-les-boutons-au-démarage-du-camtrap)
  - [Erreur corrigé](#erreur-corrigé)
          - [Remarques :](#remarques-)
___
## Introduction

Cette interface permet aux utilisateurs de se connecter à leur CamTrap (ayant un OS "bookworm") via leur réseau, en utilisant une interface web accessible depuis l'adresse suivante : [`http://raspberrypi.local:5000`](http://raspberrypi.local:5000) ou via l'adresse IP locale de votre CamTrap. L'accessibilité via le lien est possible grâce à l'outil `avahi-daemon`, qui est généralement activé par défaut.
___
## Prérequis

- Un CamTrap (ayant un OS bookworm).
- Python 3 installé sur le CamTrap.
- SSH activé sur le CamTrap.
- `scp` pour transférer les fichiers si l'interface est développée sur une machine distante.
- GPIO activé sur le Rasberry Pi.
___
## Installation

#### Étape 1 : Installation de Flask

Pour que l'interface fonctionne, Flask doit être installé sur votre CamTrap. Voici les étapes pour vérifier et installer Flask :

1. **Vérification de Flask**

    Pour vérifier si Flask est déjà installé, exécutez la commande suivante :

    ```bash
    python3 -m pip show flask
    ```

2. **Installation de `pip`**

    Si `pip` n'est pas déjà installé, installez-le avec les commandes suivantes :

    ```bash
    sudo apt update
    sudo apt install python3-pip
    sudo apt install python3-dotenv
    ```

3. **Installation de Flask**

    Ensuite, installez Flask :

    ```bash
    python3 -m pip install Flask
    ```

#### Étape 2 : Construire l'Arborescence de Fichiers

Voici l'arborescence des fichiers nécessaire pour le projet :

interface/  
├── static/  
│&emsp;&emsp;├── css/  
│&emsp;&emsp;&emsp;&emsp;└── [style.css](./static/css/style.css)  
│&emsp;&emsp;├── img/  
│&emsp;&emsp;└──  js/  
│&emsp;&emsp;&emsp;&emsp;├──[map_picker.js](./static/js/map_picker.js)  
│&emsp;&emsp;&emsp;&emsp;└── [script.js](./static/js/script.js)  
├── templates/  
│&emsp;&emsp;├── [ap_mode.html](./templates/ap_mode.html)  
│&emsp;&emsp;├── [config_app.html](./templates/config_app.html)  
│&emsp;&emsp;├── [date.html](./templates/date.html)  
│&emsp;&emsp;├── [espace_disk.html](./templates/espace_disk.html)  
│&emsp;&emsp;├── [filebrowser.html](./templates/filebrowser.html)  
│&emsp;&emsp;├── [index.html](./templates/index.html)  
│&emsp;&emsp;├── [liste_session.html](./templates/liste_session.html)  
│&emsp;&emsp;├── [new_session.html](./templates/new_session.html)  
│&emsp;&emsp;└── [wifi_mode.html](./templates/wifi_mode.html)  
├── [Readme.md](./Readme.md)  
└── [server.py](./server.py)    

- **`static/`** : Contient les images, les fichiers CSS et JavaScript.
- **`templates/`** : Contient les fichiers HTML qui seront rendus par Flask.
- **`server.py`** : Le script Python qui lance le serveur Flask.
- **`Readme.md`** : Cette documentation.

#### Étape 3 : Déploiement de l'Interface

Pour déployer l'interface, suivez ces étapes :

1. **Transfert des fichiers vers le CamTrap**

    Si vous avez développé l'interface sur une autre machine, transférez le dossier `interface/` vers le CamTrap en utilisant la commande `scp` :

    ```bash
    scp -r Documents/raspberrypi/bookworm/interface/ pi@192.168.0.104:/home/pi/Documents
    ```

2. **Lancer le serveur Flask**

    Connectez-vous au CamTrap, puis démarrez le serveur Flask en exécutant le fichier `server.py` :

    ```bash
    python3  Documents/interface/server.py
    ```

    Par défaut, l'interface sera accessible via l'adresse `http://raspberrypi.local:5000`.
___
## Détails Techniques

#### Fonctionnement de `server.py` et des Pages HTML

Le fichier **`server.py`** gère les routes et les interactions entre l’utilisateur et les pages HTML via le serveur Flask.

- **Routes Flask** : Chaque page de l'interface est reliée à une route spécifique dans `server.py`, accessible par des requêtes `GET` ou `POST` en fonction des besoins :
  - Les requêtes **`GET`** permettent d’afficher les pages, comme la page d’accueil (`index.html`).
  - Les requêtes **`POST`** sont utilisées pour envoyer des données, par exemple lors de la création de nouvelles sessions ou de configurations réseau.

- **Templates HTML** : Les fichiers HTML dans le dossier `templates/` sont rendus par Flask à l'aide de la fonction `render_template`, permettant une séparation claire entre le code Python et le contenu HTML.

#### Utilisation du Map Picker (en mode WiFi)

L'interface utilise un **Map Picker** pour la sélection de localisation, implémenté avec **Leaflet.js**, une bibliothèque JavaScript populaire pour des cartes interactives.

- **Fonctionnalités** : Les utilisateurs peuvent cliquer sur une carte pour sélectionner des coordonnées géographiques, qui sont ensuite envoyées au serveur pour traitement.
- **Documentation Leaflet** : Pour plus d’informations sur la personnalisation et les fonctionnalités de Leaflet.js, consultez la [documentation officielle](https://leafletjs.com/).
___

## Utilisation

1. Assurez-vous que le CamTrap est connecté au même réseau que votre ordinateur.
2. Ouvrez un navigateur web et accédez à l'URL suivante : [`http://raspberrypi.local:5000`](http://raspberrypi.local:5000).
3. Utilisez les fonctionnalités proposées pour interagir avec le CamTrap, comme la navigation de fichiers ou la configuration réseau.

### Mode de Fonctionnement du CamTrap

Le CamTrap est équipé d'un bouton permettant de sélectionner le mode de fonctionnement (Voir la [Documentation](GPIO.md)):

- **Mode Wi-Fi (0)** : Si le bouton est positionné sur **0**, le CamTrap démarre en mode Wi-Fi standard, se connectant à votre réseau sans fil configuré.
- **Mode AP (1)** : Si le bouton est positionné sur **1**, le CamTrap démarre en mode Point d'Accès (AP), permettant aux autres appareils de se connecter directement au CamTrap.git p

Assurez-vous de régler le bouton selon vos besoins avant de démarrer le CamTrap pour utiliser l'interface web appropriée.

### Navigation de Fichiers avec FileBrowser

Le CamTrap permet également de naviguer et de gérer les fichiers directement via une interface web : 

- Visualisation des fichiers et dossiers présents sur le CamTrap.
- Téléchargement et gestion des fichiers via l'interface.
- Accès à des fonctionnalités de recherche et de tri pour faciliter l'utilisation.

Pour l'installation (Voir la [Docummentation](filebrowser.md)).
___

##### Modification des droits 
```bash
sudo chmod +x interface/server.py
```

___

## Configuration de la mise en route du serveur et du script pour les boutons au démarage du CamTrap
```bash
sudo nano /etc/rc.local
```
1. /etc/rc.local :
```
python3 /home/pi/wifi_ap_gpio.py &

python3 /home/pi/Documents/interface/server.py &
```
> :warning: **Rappel :**  Le contenu de [wifi_ap_gpio.py](GPIO.md#rédaction-du-script-permettant-de-passer-le-raspberry-pi-en-mode-wifi-ou-en-mode-ap-en-fonction-de-la-position-du-bouton)
2. reboot
```bash
sudo reboot
```
3. Voir status :
```bash
systemctl status rc-local
```
4. Voir logs : 
```bash
journalctl -u rc-local
```
commandes disponnibles: 
- aller à la fin du fichier : maj+g
- fermer : q

## Erreur corrigé

###### Remarques :

Au démarrages les pins ne sont pas configurées, ce qui explique pourquoi les LED sont allumées par défaut. Lorsqu'une session est lancée, les pins se configurent correctement. Ainsi, si la session est arrêtée, les LED s'éteignent automatiquement.