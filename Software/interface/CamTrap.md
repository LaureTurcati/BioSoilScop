# CampTrap

> **Introduction :** CampTrap est une solution permettant de gérer un Raspberry Pi configuré en différents modes pour des utilisations spécifiques.

## Table des matières
1. [Introduction](#introduction)
2. [Quick start](#quick-start)
3. [CamTrap](#raspberry-pi)
    - [Étape 1 : Démarrage du CamTrap](#étape-1--démarrage-du-raspberry-pi)
    - [Étape 2 : Lancement de l'interface](#étape-2--lancement-de-linterface)
4. [Page d'accueil](#page-daccueil)
5. [Mode de Connexion](#mode-de-connexion)
6. [Configuration de l'Application](#configuration-de-lapplication)
7. [Configuration de la Date](#configuration-de-la-date)
8. [Filebrowser](#comment-avoir-accès-au-photos-)
9. [Conclusion](#conclusion)

___
## Introduction
**L'interface** est conçu pour faciliter l'utilisation et la configuration de votre CamTrap.
___
## Quick Start

### Étape 1 : Préparation

1. **Positionnez le bouton de mode de fonctionnement** sur :
   - **0** pour le mode Wi-Fi
   - **1** pour le mode Point d'Accès (AP)
   > Pour le premier démarrage, mettez le bouton sur **1** (mode AP).

### Étape 2 : Connexion au Raspberry Pi
1. **Allumez le Raspberry Pi** en vérifiant que le bouton est bien positionné.
2. **Connectez votre ordinateur** au bon Wi-Fi.

### Étape 3 : Accéder à l'interface web
1. **Ouvrez un navigateur web** sur votre ordinateur.
2. **Accédez à l'URL** suivante : [`http://raspberrypi.local:5000`](http://raspberrypi.local:5000).

### Étape 4 : Configuration initiale
1. **Configurez la date** via l'onglet **Configuration de la Date** pour garantir le bon fonctionnement.
2. **Accédez à l'onglet "Mode de Connexion"** pour choisir et configurer votre réseau Wi-Fi.
3. **Configuration de l'app** 
4. **Acceder au dossiers photo** en démarant le service permettant d'avoir accès au 'drive' des documents et l'ouvrir via l'onglet Filebrowser.

___
## CamTrap

### Étape 1 : Démarrage du CamTrap
Votre CamTrap est équipé d'un bouton permettant de sélectionner le mode de fonctionnement :

- **Mode Wi-Fi (0)** : Si le bouton est positionné sur **0**, le CamTrap démarre en mode Wi-Fi standard, se connectant à votre réseau sans fil configuré.
- **Mode AP (1)** : Si le bouton est positionné sur **1**, le CamTrap démarre en mode Point d'Accès (AP), permettant aux autres appareils de se connecter directement au CamTrap.

> :warning: **Attention :** Pour le premier démarrage, choisissez le mode **AP** car le Wi-Fi n'est pas encore configuré.

Assurez-vous de régler le bouton selon vos besoins avant de démarrer le CamTrap pour utiliser l'interface web.

### Étape 2 : Lancement de l'interface
1. Assurez-vous que le CamTrap est connecté au même réseau que votre ordinateur.
2. Ouvrez un navigateur web et accédez à l'URL suivante : [`http://raspberrypi.local:5000`](http://raspberrypi.local:5000).

___

## Page d'accueil

Contient des informations sur le projet.
___
## Mode de Connexion

#### Mode Wi-FI
- Permet de passer le CamTrap en mode **Wi-Fi** en utilisant le bouton.

#### Mode AP
- Affichage des réseaux déjà associés
- Passage en mode **Wi-Fi**
- Ajout d'un réseau Wi-Fi (ce qui connecte le CamTrap au nouveau réseau Wi-Fi associé)
___
## Configuration de l'Application
L'onglet **Configuration de l'Application** permet de modifier les paramètres de la caméra. Voici les différents paramètres configurables :

- **Gain** : Permet de régler le niveau de gain pour ajuster la sensibilité de la caméra à la lumière, utile dans des environnements à faible luminosité.
*Valeur par défaut : 0*
- **Exposure** : Contrôle l'exposition pour équilibrer la luminosité de l'image, en ajustant la durée pendant laquelle la caméra capture la lumière.
*Valeur par défaut : normal*
- **HDR** : Active ou désactive le mode High Dynamic Range (HDR) pour capturer une plage plus large de luminosité, permettant de mieux gérer les scènes avec des contrastes élevés.
*Valeur par défaut : off*
- **Brightness** : Ajuste la luminosité générale de l'image, influençant la clarté de la scène.
*Valeur par défaut : 0*
- **Contrast** : Modifie le contraste entre les parties sombres et claires de l'image pour ajouter de la profondeur et du détail.
*Valeur par défaut : 1*
- **Saturation** : Contrôle l'intensité des couleurs dans l'image, utile pour obtenir des couleurs vives ou plus naturelles.
*Valeur par défaut : 1*
- **Autofocus Mode** : Sélectionne le mode de mise au point automatique, comme le mode continu ou ponctuel, en fonction de la nature des sujets à capturer.
*Valeur par défaut : default*
- **Autofocus Range** : Définit la plage de distance sur laquelle l'autofocus doit fonctionner, comme le mode proche ou éloigné, selon les besoins de la prise de vue.
*Valeur par défaut : normal*
- **Autofocus Speed** : Ajuste la vitesse de l'autofocus, pour une mise au point rapide ou plus lente, adaptée aux sujets statiques ou en mouvement.
*Valeur par défaut : normal*

___
## Configuration de la Date 
L'onglet **Configuration de la Date** permet de vérifier et de mettre à jour la date et l'heure du CamTrap.

- **Affichage de la date actuelle** : La date et l'heure actuelles du CamTrap sont affichées.
- **Mise à jour de la Date** : Lors de l'utilisation du CamTrap après une longue période d'inactivité, il est important de vérifier et de mettre à jour la date pour assurer le bon fonctionnement des services réseau et des certificats.

#### Comment mettre à jour la date :
1. Rendez-vous sur l'onglet **Configuration de la Date**.
2. Vérifiez la date affichée.
3. Utilisez le formulaire pour entrer la date correcte si nécessaire.
___
## Sessions

#### Nouvelle session
L'onglet **Création de session** offre un formulaire pour définir une nouvelle session de prise de vue. Vous pouvez choisir de configurer la session :
- **En continu** : pour une capture de photos sans interruption.
- **Sur une plage horaire** : en spécifiant des créneaux horaires ainsi que des dates de début et de fin.

De plus, il est possible d’associer plusieurs informations à chaque session, telles qu’une description et la position géographique du CamTrap.

#### Liste des sessions
L'onglet **Liste des sessions** permet d'afficher un tableau des différentes sessions existantes. À partir de cet onglet, vous pouvez :
- **Démarrer une session** : lancé la capture de photos pour une nouvelle session.
- **Stopper une session** : arrêter la capture de photos en cours.
- **Supprimer une session** : retirer une session qui n'est plus nécessaire.
___
## Comment avoir accès au photos ?
L'onglet Filebrowser va nous permettre de démarrer un service nous permettant d'avoir accès aux dossiers photos.
1. Démarrage du service Filebrowser
2. Ouverture dans un autre onglet du 'drive'
3. Identifiant : admin | Password : admin
___

## Conclusion
Ce guide vise à vous aider à démarrer et à utiliser **L'interface** de manière optimale.
