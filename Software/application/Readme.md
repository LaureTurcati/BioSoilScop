# Application de Capture de Photos

## Table des Matières
1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Structure du Projet](#structure-du-projet)
4. [Configuration des Environnements](#configuration-des-environnements)
5. [Fonctionnalités](#fonctionnalités)
    - [Démarrage du Programme](#démarrage-du-programme)
    - [Session en Mode "Continue"](#session-en-mode-continue)
    - [Session en Mode "Plage"](#session-en-mode-plage)
    - [Detection des objets mobiles](#detection-des-objets-mobiles)

___
## Introduction

Cette application permet de capturer des photos en fonction de la détection de mouvement et de luminosité. Elle utilise une caméra, un capteur de luminosité (ADS1115), et des fichiers de configuration pour ajuster son comportement.

___
## Prérequis

Pour exécuter l'application, vous devez disposer des éléments suivants :

- **Python 3** installé sur le système CamTrap.
- **SSH** activé sur le CamTrap pour un accès distant.
- L'outil `scp` pour transférer les fichiers si vous développez sur une machine distante.

___
## Structure du Projet

Voici l'organisation des fichiers et dossiers principaux :

home/  
├── ADS1115/  
├── app/  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [ \_\_init\_\_.py](./__init__.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [ads_luminosity.py](./ads_luminosity.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [camera.py](./camera.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [config.py](./config.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [image.py](./image.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [log.py](./log.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [luminosity.py](./luminosity.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [motion.py](./motion.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [script.py](./script.py)  
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [session.py](./session.py)
│&emsp;&emsp;&nbsp;&nbsp;&nbsp;├── [set_video.py](./set_video.py)
└── &emsp;└── [Readme.md](./Readme.md)  


___
## Configuration des Environnements

### Environnement ADS1115
Pour le capteur de luminosité :

```bash
sudo python3 -m venv ads1115
source ads1115/bin/activate
sudo pip3 install adafruit-circuitpython-ads1x15
```

### Environement Global

```bash
sudo apt install libcamera-apps python3-libcamera python3-picamera2
sudo apt install python3-rpi.gpio
sudo apt install python3-opencv opencv-data ffmpeg
sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip
```

___
## Fonctionnalités

### Sessions
L'application utilise les fichiers de configuration situés dans `home/camtrap/config.json` pour configurer la caméra. Elle dispose de deux modes principaux : **"continue"** et **"plage"**.

#### Démarrage du Programme

##### Récupération des paramètres :

- Charger les paramètres de la session.
- Ajouter un log indiquant le chargement des paramètres.

##### Initialisation des variables :

- Charger les paramètres généraux, de la caméra, et de luminosité.
- Ajouter un log confirmant l'initialisation.

#### Session en Mode "Continue"

##### Initialiser les threads :

- Configurer et démarrer la caméra en mode continu (ajouter un log).
- Démarrer le capteur de luminosité avec l'environnement ADS1115 (ajouter un log).

##### Boucle principale :

- **Vérifier la luminosité :**
  - Si elle est inférieure à `th_jour` : passer en mode nuit (log ajouté).
  - Si elle est supérieure à `th_nuit` : passer en mode jour (log ajouté).
- **Détecter les mouvements :**
  - Si un mouvement est détecté, capturer une photo (log ajouté).

#### Session en Mode "Plage"

##### Initialiser les threads :

- Configurer et démarrer la caméra en mode continu (ajouter un log).
- Démarrer le capteur de luminosité avec l'environnement ADS1115 (ajouter un log).

##### Boucle principale :

- **Vérifier si le jour actuel est dans la plage définie** (`jour_debut` à `jour_fin`) :
  - Si oui, vérifier les créneaux horaires définis dans `time_slots` :
    - Si l'heure actuelle correspond à un créneau, continuer.
    - **Vérifier la luminosité :**
      - Si elle est inférieure à `th_jour` : passer en mode nuit (log ajouté).
      - Si elle est supérieure à `th_nuit` : passer en mode jour (log ajouté).
    - **Détecter les mouvements :**
      - Si un mouvement est détecté, capturer une photo (log ajouté).

#### Detection des objets mobiles
- La prise de photos dans la classe Image est pilotée par la détection d'insectes par une instance de la classe Detector.
- La classe detector permet d'identifier la présence d'objets mobiles dans le champ, de les distinguer d'un "background" et d'en mesurer la taille et la vitesse.
    - Identification du background 
        - L'intérêt est de séparer les mouvements d'insectes des changements de luminosité ou autres mouvements parasites (ex : brins d'herbe qui bougent)
        - Mise à jour du background avec un algorithme de soustraction de fond (BackgroundSubtractorMOG2 de OpenCV)
        - Le background est mis à jour pendant un certain nombre d'images (paramétrable) avant d'être considéré comme stable.
        - Le background est réinitialisé régulièrement, notamment après chaque prise de photos afin de s'adapter aux changements de luminosité.
    - Détection de présente d'objets mobiles
        - Retrait du background de l'image courante
        - Calcul de vitesse en comparant deux images successives
        - Identification des objets mobiles par détection de contours ou de blobs
            - Détection de contours : identifications de gradients (Canny) + fermeture morphologique (identifications de "bords contigus") + approximation de polygone + calcul d'aire 
            - Détection de blobs : SimpleBlobDetector (OpenCV) + calculd'aire
        - Filtrage des objets selon leur taille et leur vitesse 
- Deux threads distincts sont utilisés pour mettre à jour le background en permalence et effectuer la détection à intervalles réguliers.  
- Paramètres ajustables :
    - Vitesse minimale et maximale à considérer : min_shape_speed, max_shape_speed (px/sec)
    - Taille minimale et maximale à considérer : min_shape_area, max_shape_area (px^2)
    - Background :
        - Nombre d'images avant que le fond soit considéré comme stable : pictures_before_bg_is_set
        - Taille de l'historique pour le modèle de fond : history 
    - Méthode de détection : contours ou blobs (blobs semble bien mieux fonctionner)
        - Blobs : 
            - flou : blur_kernel (~5)
            - inertie de la forme (allongée/circulaire) : minInertiaRatio (~0.1), maxInertiaRatio (~1) 
        - Contours : 
            - flou : blur_kernel (~9)
            - Canny : canny_threshold_1 (~14), canny_threshold_2 (~36)
            - Fermeture morphologique : closing_kernel (~5), closing_iterations (~1)


### Capture Vidéo

``` bash
ffplay -f rawvideo -pixel_format yuv420p -video_size 1536x864 <nom_video>
ffplay -f rawvideo -pixel_format yuv420p -video_size 640x480 <nom_video>
```

#### Paramètres disponibles
- **Qualité vidéo** : Choix entre **Low** et **High**.
- **Intensité des LEDs** : Ajustez l'intensité des LEDs selon vos préférences.
- **Durée de la vidéo** : La durée maximale de la vidéo est de **60 secondes**.

De plus, la caméra ce paramètre en utilisant le fichier de config `/home/pi/camtrap/config.json`

##### Fichier vidéo généré
En fonction du choix de la qualité vidéo, la caméra génère un fichier `.raw`, qui est un fichier vidéo brut. Le format du fichier dépend des critères suivants :
- Taille (size)
- Format
- Encodeur (généralement `null`)

#### Pré-requis

Avant de commencer, assurez-vous que **ffplay** est installé sur votre machine.

- Version requise : `5.1.6` ou supérieure.

#### Lecture du fichier `.raw`

Une fois la vidéo capturée, vous pouvez la lire avec **ffplay** en utilisant les commandes suivantes, adaptées à la qualité choisie :

- Pour une vidéo en qualité **High** (1536x864) :
  ```bash
  ffplay -f rawvideo -pixel_format yuv420p -video_size 1536x864 <nom_video>
  ```
- Pour une vidéo de qualité **Low** (640x864) :
  ```bash
  ffplay -f rawvideo -pixel_format yuv420p -video_size 640x480 <nom_video>
  ```

___
## Paramètre de la caméra

Voir les [paramètres](./Parametres.md).

