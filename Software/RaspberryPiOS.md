# Installation d'un OS sur un Raspberry Pi avec Raspberry Pi Imager

Ce guide est un rappel pour installer un OS sur un Raspberry Pi en utilisant **Raspberry Pi Imager** sous Ubuntu.

---

## 1. Installation de Raspberry Pi Imager

### 1.1 Via le Store Ubuntu

1. Ouvrir le **Store Ubuntu**.
2. Rechercher et installer **Raspberry Pi Imager**.

### 1.2 Installation manuelle via fichier .deb

1. Télécharger le fichier `.deb` depuis le site officiel : [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
   - Exemple de fichier : `imager_x.x.x_amd64.deb`
2. Ouvrir un terminal et exécuter les commandes suivantes :

    ```bash
    cd ~/Téléchargements
    sudo apt install ./imager_x.x.x_amd64.deb
    ```

---

## 2. Télécharger et flasher l'OS

### 2.1 Utilisation de Raspberry Pi Imager

1. Ouvrir **Raspberry Pi Imager**.
2. Rechercher et sélectionner l'OS souhaité dans la liste proposée.

### 2.2 Si l'OS n'est pas disponible dans la liste

1. Télécharger l'image `.zip` de l'OS depuis un site officiel.
2. (Optionnel) Vérifier l'intégrité du fichier téléchargé en comparant le **hash SHA256**.

#### Vérification du fichier avec SHA256

- Télécharger également le fichier `.zip.sha256`.
- Calculer le hash du fichier téléchargé :

    ```bash
    sha256sum ./chemin/vers/fichier.zip
    ```

- Comparer le résultat avec le contenu du fichier `.zip.sha256` :

    ```bash
    diff <(sha256sum ./chemin/vers/fichier.zip) fichier.sha256
    ```

Si le hash est correct, vous pouvez continuer.

### 2.3 Flash de l'OS sur la carte SD

1. Insérer la **carte SD** du Raspberry Pi dans le PC.
2. Dans **Raspberry Pi Imager**, choisir **"Use custom"** pour sélectionner l'image téléchargée.
3. Sélectionner la **carte SD** comme destination de l'écriture.
4. Cliquer sur **"Écrire"** pour flasher l'OS.

---

## 3. Préparer le Raspberry Pi

1. Retirer la carte SD du PC et l'insérer dans le Raspberry Pi.
2. Démarrer le Raspberry Pi.

### 3.1 Mettre à jour le Raspberry Pi

1. Mettre à jour la date du système (si nécessaire) :

    ```bash
    sudo date -s 'yyyy-mm-dd hh:mm:ss'
    ```

2. Mettre à jour les paquets du système :

    ```bash
    sudo apt update
    sudo apt upgrade
    ```