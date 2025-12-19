import sys
import os
import time
import json
import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import Encoder
from picamera2.outputs import FileOutput


# Vérifier si les 3 arguments a été fourni
if len(sys.argv) != 4:
    print("Utilisation : python3 set_video.py <resolution> <luminosite> <time>")
    sys.exit(1)

quality = sys.argv[1].lower()
luminosite = int(sys.argv[2])
video_time = int(sys.argv[3])

LED_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
PI_PWM = GPIO.PWM(LED_PIN,1000)
PI_PWM.start(0)	

if 0 <= luminosite <= 100:
    PI_PWM.ChangeDutyCycle(luminosite)
else:
    print("La luminosité doit être comprise entre 0 et 100.")
    sys.exit(1)

config_file = "/home/pi/camtrap/config.json"

try:
    with open(config_file, "r") as file:
        config = json.load(file)  # Lire le JSON et le convertir en dictionnaire Python
except Exception as e:
    print(f"Erreur lors de la lecture du fichier de configuration : {e}")
    sys.exit(1)

# Initialiser la caméra
cam = Picamera2()

if quality == "hires":
    video_config = cam.create_video_configuration(main={"size": (1536, 864), "format":"YUV420"}, encode="main")
    size = "1536x864"
elif quality == "lores":
    video_config = cam.create_video_configuration(lores={"size": (640, 480), "format":"YUV420"}, encode="lores")
    size = "640x480"

cam.configure(video_config)
cam.set_controls({
    "Brightness": config.get("brightness", 0),
    "Contrast": config.get("contrast", 0),
    "Saturation": config.get("saturation", 0),
    "AeExposureMode": config.get("exposure", 0),
    "AnalogueGain": config.get("gain", 0),
    "HdrMode": config.get("hdr", 0),
    "AfMode": config.get("autofocus_mode", 0),
    "AfSpeed": config.get("autofocus_speed", 0),
    "AfRange": config.get("autofocus_range", 0)
})


# Définir le chemin de sortie
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format YYYYMMDD_HHMMSS
filename = f"video_{timestamp}_{size}_yuv420p_{video_time}s"

video_dir = "/home/pi/camtrap/videos"
os.makedirs(video_dir, exist_ok=True)

raw_path = f"{video_dir}/{filename}.raw"



# Initialiser l'encodeur (null)
encoder = Encoder()

# Démarrer l'enregistrement sur le bon flux
cam.start_recording(encoder, FileOutput(raw_path))
print(f"Enregistrement en {quality} qualité...")

try:
    time.sleep(video_time)

finally:
    # Arrêter l'enregistrement
    cam.stop_recording()
    print("Enregistrement terminé.")
    # 
    PI_PWM.stop()  # Arrêter le PWM
    GPIO.cleanup()  # Réinitialiser les GPIO