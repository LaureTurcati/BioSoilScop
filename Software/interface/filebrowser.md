# Installer filebrowser sur Raspberry pi 

___
## 1. Installation de FileBrowser
```bash
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
```
___
## 2. Lancer filebrowser sur Raspi 
```bash
filebrowser -p 8080 -a 192.168.0.104 -r /home/pi 
```

<font color='blue'>-p : spécifie le port sur lequel FileBrowser va écouter (ici, 8080)</font>.
<font color='red'>-a : définit l'adresse IP à laquelle le service sera lié (ici, 192.168.0.104)</font>.
<font color='green'>-r : désigne le dossier racine pour la navigation (ici, /home/pi)</font>.

___
## 3. Accéder à FileBrowser depuis un PC
http://192.168.0.104:8080/

identifiant par défaut: admin
password par défaut: admin
