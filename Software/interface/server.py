from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import os
import subprocess
import netifaces as ni
import json
import shutil
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY')
# -------------------------------------------------- Fonctions --------------------------------------------------

# Fonction qui verifie le mode actuel du WiFi (AP ou client)
def check_wifi_mode():
    mode = os.popen('iw dev wlan0 info | grep -q "type AP" && echo "AP" || echo "WiFi"').read().strip()
    return mode

# Fonction qui retourne le SSID du WiFi actuellement utilise
def check_wifi_utilise():
    result = subprocess.run("nmcli -t -f active,ssid dev wifi | grep '^oui' | cut -d':' -f2", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wifi_utilise = result.stdout.strip()
    return wifi_utilise

# Fonction qui retourne le(s) SSID du(es) WiFi actuellement associes
def check_wifi_dispo():
    result = subprocess.run("nmcli -t -f name,type,device con | grep wireless | grep -v 'wlan0'", shell=True, stdout=subprocess.PIPE, text=True)
    wifi_dispo = [line.split(':')[0] for line in result.stdout.splitlines() if line]
    return wifi_dispo

# Fonction qui retourne les wifi à proximite et qui ne sont pas dejà associes
def check_wifi_proximity():
    wifi_associes_result = subprocess.run('nmcli -t -f NAME con show', shell=True, stdout=subprocess.PIPE, text=True)
    wifi_associes_ssids = set(wifi_associes_result.stdout.splitlines())
    wifi_proxi_result = subprocess.run('nmcli -t -f SSID device wifi list', shell=True, stdout=subprocess.PIPE, text=True)
    wifi_proxi_ssids = wifi_proxi_result.stdout.splitlines()
    wifi_proxi = [ssid for ssid in wifi_proxi_ssids if ssid.strip() and ssid not in wifi_associes_ssids]
    return wifi_proxi[:5]

# Fonction qui permet d'ajouter un wifi et de ce connecter dessus
def ajouter_wifi(ssid,password):
    subprocess.run(['sudo','nmcli', 'device', 'wifi', 'connect', ssid ,'password', password])

# Fonction qui permet de modifier la date du raspberry pi
def remplacer_date(date, hour):
    nouvelle_date_heure = f"{date} {hour}"
    subprocess.run(['sudo', 'date', '-s', nouvelle_date_heure])

# Fonction qui permet de recuperer l'adresse ip du raspberry pi
def get_ip_address(interface):
    try:
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        return ip
    except KeyError:
        return None

def concatener_dms(direction, degres, minutes, secondes=0):
    return f"{degres}°{minutes}'{secondes}\" {direction}"

def concatener_dmm(direction, degres, minutes):
    return f"{degres}°{minutes}' {direction}"

def liste_session():
    base_directory = "/home/pi/camtrap"
    json_files = [] 
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".json"):
                folder_name = os.path.basename(root)
                expected_file_name = f"{folder_name}.json"
                if file == expected_file_name:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file) 
                            json_files.append({"path": file_path, "data": data}) 
                    except json.JSONDecodeError:
                        print(f"Erreur de décodage JSON pour le fichier: {file_path}") 
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier {file_path}: {e}") 
    return json_files

def update_status(filename, new_status):
    file_path = f'/home/pi/camtrap/{filename}/{filename}.json'
    if not os.path.exists(file_path):
        return render_template('liste_session.html', message='Erreur : Fichier non trouvé')
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        data['status'] = new_status
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return redirect(url_for('liste'))
    except Exception as e:
        return render_template('liste_session.html', message=f'Erreur : {str(e)}')

def load_config():
    file_path = '/home/pi/camtrap/config.json'
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}  # Retourne un dictionnaire vide si le fichier n'existe pas
    except json.JSONDecodeError:
        return {} 

# -------------------------------------------------- Routes --------------------------------------------------

# Route principale qui sert de page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher la bonne page et recupperer les bonnes informations
@app.route('/mode')
def mode():
    mode = check_wifi_mode()
    if mode == "AP":
        wifi_dispo = check_wifi_dispo()
        wifi_proxi = check_wifi_proximity()
        return render_template('ap_mode.html', wifi_dispo=wifi_dispo, wifi_proxi=wifi_proxi)
    else:
        wifi_utilise = check_wifi_utilise()
        return render_template('wifi_mode.html', wifi_utilise=wifi_utilise)

# Route pour ajouter une connection wifi via les donnees du formulaire
@app.route('/configurer_wifi', methods=['POST'])
def configurer_wifi():
    ssid = request.form['wifi']
    password = request.form['password']
    if ssid and password:
        ajouter_wifi(ssid, password)
        return render_template('ap_mode.html')
    else:
        return "Veuillez entrer un SSID et un mot de passe", 400

# Route pour changer le raspberry en mode AP via un script
@app.route('/set_ap_mode')
def set_ap_mode():
    os.system('sudo /home/pi/bookworm_wifi_ap_switch.sh ap') 
    return redirect('/')

# Route pour changer le raspberry en mode Wi-Fi via un script
@app.route('/set_wifi_mode')
def set_wifi_mode():
    os.system('sudo /home/pi/bookworm_wifi_ap_switch.sh wifi') 
    return redirect('/')

# Route pour afficher la page de configuration de l'app
@app.route('/config_app')
def config_app():
    config_data = load_config()
    return render_template('config_app.html', config=config_data)


@app.route('/save_config', methods=['POST'])
def conf_json():
    form_data = request.form.to_dict()
    file_path = '/home/pi/camtrap/config.json'
    expected_types = {
        "nom": str,
        "gain": int,
        "exposure": int,
        "hdr": int,
        "brightness": float,
        "contrast": int,
        "saturation": float,
        "autofocus-range": int,
        "autofocus-mode": int,
        "autofocus-speed": int,
        "th-jour": float,
        "th-nuit": float,
        "motion-detect-threshold": int,
        "mov-area": int,
        "vib-threshold": int,
        "hq-iteration": int,
        "interval": int,
    }
    converted_data = {}
    try:
        for key, value in form_data.items():
            expected_type = expected_types.get(key, str) 
            try:
                converted_data[key] = expected_type(value)  
            except ValueError:
                converted_data[key] = value
                print(f"Erreur de conversion pour la clé '{key}' avec valeur '{value}'")
    except Exception as e:
        return render_template(
            'config_app.html',
            message=f"Erreur lors de la conversion des données: {str(e)}"
        )
    try:
        with open(file_path, 'w') as json_file:
            json.dump(converted_data, json_file, indent=4)
        return render_template('config_app.html', message=f'Fichier de configuration créé avec succès !')
    except Exception as e:
        return render_template('config_app.html', message=f"Erreur lors de la création du fichier de configuration: {str(e)}")

# Route pour afficher la page de configuration de la session
@app.route('/new_session')
def config_session():
    mode = check_wifi_mode()
    return render_template('new_session.html', mode=mode)


# Route pour créer un fichier session en json via un formulaire
@app.route('/save_session', methods=['POST'])
def construire_json():
    form_data = request.form.to_dict()
    if 'latDirection' in form_data and 'latDegrees' in form_data and 'latMinutes' in form_data and 'latSeconds' in form_data:
        # Format DMS (Degrés, Minutes, Secondes)
        latitude = concatener_dms(form_data['latDirection'], form_data['latDegrees'], form_data['latMinutes'], form_data['latSeconds'])
        longitude = concatener_dms(form_data['lngDirection'], form_data['lngDegrees'], form_data['lngMinutes'], form_data['lngSeconds'])
    elif 'latDirection' in form_data and 'latDegrees' in form_data and 'latMinutesDecimal' in form_data:
        # Format DMM (Degrés, Minutes Décimaux)
        latitude = concatener_dmm(form_data['latDirection'], form_data['latDegrees'], form_data['latMinutesDecimal'])
        longitude = concatener_dmm(form_data['lngDirection'], form_data['lngDegrees'], form_data['lngMinutesDecimal'])
    elif 'latitude' in form_data and 'longitude' in form_data:
        # Format DD (Degrés Décimaux)
        latitude = form_data['latitude']
        longitude = form_data['longitude']
    else:
        return render_template('new_session.html', message="Erreur : Format de coordonnées non reconnu.")

    name = form_data.get('nom_session').replace(' ', '_')
    dir_path = f'/home/pi/camtrap/{name}'
    file_path = f'{dir_path}/{name}.json'
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            return render_template('new_session.html', message=f"Erreur lors de la création du répertoire: {str(e)}")
    
    if os.path.exists(file_path):
        return render_template('new_session.html', message=f"Erreur : le fichier '{name}.json' existe déjà.")
    
    form_data['latitude'] = latitude
    form_data['longitude'] = longitude

    form_data['status'] = 'stop'

    if form_data.get('choix') == 'plage':
        time_slots = []
        for i in range(10):
            time_debut = form_data.get(f'time_debut_{i}')
            time_fin = form_data.get(f'time_fin_{i}')
            if time_debut and time_fin:
                time_slots.append({
                    'time_debut': time_debut,
                    'time_fin': time_fin
                })
        form_data['time_slots'] = time_slots
    elif form_data.get('choix') == 'continue':
        form_data['time_slots'] = [] 

    try:
        with open(file_path, 'w') as json_file:
            json.dump(form_data, json_file, indent=4)
        return render_template('new_session.html', message=f'Fichier JSON créé avec succès à {file_path}')
    except Exception as e:
        return render_template('new_session.html', message=f"Erreur lors de la création du fichier JSON: {str(e)}")

@app.route('/liste_session')
def liste():
    date_bash = subprocess.check_output(['date']).decode('utf-8').strip()
    files = liste_session()
    return render_template('liste_session.html', files=files, date=date_bash)

@app.route('/delete_file', methods=['POST'])
def delete_file():
    file_path = request.json.get('file_path')
    if file_path:
        try:
            if os.path.exists(file_path):
                folder_path = os.path.dirname(file_path)
                subprocess.run(['sudo', 'rm', '-r', folder_path], check=True)
                return jsonify({"message": "Dossier supprimé avec succès"}), 200
            else:
                return jsonify({"error": "Le fichier n'existe pas"}), 404
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Erreur lors de la suppression: {str(e)}"}), 500
    else:
        return jsonify({"error": "Chemin du fichier non fourni"}), 400

@app.route('/start_session/<filename>', methods=['POST'])
def start_session(filename):
    correct_filename = filename.replace(' ', '_')
    file_path = f'/home/pi/camtrap/{correct_filename}/{correct_filename}.json'
    try: 
        subprocess.Popen(['python3', '/home/pi/app/script.py', file_path])
        print("Script lancé")
        flash(f'Session {filename} démarrée.', 'success')
    except Exception as e:
        print(f"Erreur lors du lancement du script : {e}")
        flash(f'Erreur : Échec du lancement de la session {filename}.', 'error')
    response = update_status(correct_filename, 'start')
    return response

@app.route('/stop_session/<filename>', methods=['POST'])
def stop_session(filename):
    correct_filename = filename.replace(' ', '_')
    try: 
        subprocess.run(['pkill', '-f', f'{correct_filename}.json'], check=True)
        print("Script arrêté")
        flash(f'Session {filename} arrêtée.', 'success')
    except Exception as e:
        print(f"Erreur lors du lancement du script : {e}")
        flash(f'Erreur : L’arrêt du script a échoué : {e}', 'error')
    response = update_status(correct_filename, 'stop')
    return response 

@app.route('/any_active_session', methods=['GET'])
def any_active_session():
    """Retourne true si une session est en cours, sinon false."""
    sessions = liste_session()
    active_session = any(file['data'].get('status') == 'start' for file in sessions)
    return jsonify({"active": active_session})   
    

# Route pour afficher la page date
@app.route('/date')
def date():
    date_bash = subprocess.check_output(['date']).decode('utf-8').strip()
    return render_template('date.html', date=date_bash)

# Route pour configurer la date du raspberry via un formulaire
@app.route('/config_date', methods=['POST'])
def config_date():
    date = request.form['date']
    hour = request.form['hour']
    if date and hour:
        remplacer_date(date, hour)
        return render_template('date.html', date=f"Date du Raspberry: {date} {hour}")
    else:
        return "Veuillez entrer une date et une heure", 400


# Route pour afficher la page filebrowser
@app.route('/filebrowser')
def filebrowser():
    return render_template('/filebrowser.html')

# Route pour demarrer le service filebrowser
@app.route('/start_filebrowser', methods=['POST'])
def start_filebrowser():
    ip = get_ip_address('wlan0')
    
    if ip is None:
        raise ValueError("Impossible de récupérer l'adresse IP de wlan0")

    port = '8080'
    path = '/home/pi/camtrap'
    subprocess.Popen(['filebrowser', '-p', port, '-a', ip, '-r', path])
    return jsonify({"message": "Filebrowser a été activé"}), 200

# Route pour obtenir l'URL de Filebrowser et l'ouvrir dans un autre onglet
@app.route('/open_filebrowser')
def open_filebrowser():
    ip = get_ip_address('wlan0')
    port = '8080'
    if ip:
        url = f'http://{ip}:{port}'
        return jsonify({"url": url}), 200  
    return jsonify({"error": "Erreur: Impossible de récupérer l'adresse IP."}), 500

@app.route('/espace_disk')
def  espace_disk():
    total, used, free = shutil.disk_usage('/')
    percentage_free = (free / total) * 100
    print(f"Percentage Free: {percentage_free}")
    return render_template('espace_disk.html', percentage_free=percentage_free)

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/set_video', methods=['POST'])
def start_video():
    resolution = request.form['resolution']
    luminosite = request.form['led']
    time = request.form['time']

    try :
        subprocess.Popen(['python3', '/home/pi/app/set_video.py', resolution, luminosite, time])
        print("Script lancé")
    except Exception as e:
        print(f"Erreur lors du lancement du script : {e}")
    return render_template('video.html')


# -------------------------------------------------- Lancement du serveur Flask --------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
