from time import sleep
import RPi.GPIO as GPIO
import threading
import sys
from datetime import datetime

from log import LOG
from config import Config
from session import Session
from camera import Camera
from luminosity import Luminosity
from image import Image
from detector import Detector
from threading import Thread, Lock

#local constants
PIN_INTER = 26
DEBUG_LEVEL = 1
# 0: ERROR
# 1: INFO
# 2: FULL DEBUG


# gpio setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_INTER, GPIO.OUT)
PI_PWM = GPIO.PWM(PIN_INTER,1000)
PI_PWM.start(0)	


# cleanup function
def cleanup():
    PI_PWM.stop()
    GPIO.cleanup()

# main function
if __name__ == "__main__":
    print("Démarrage du script...")
    if len(sys.argv) < 2:
        print("Erreur : aucun fichier de session fourni.")
        sys.exit(1)

    session_file = sys.argv[1]
    camera = None
    luminosity = None
    motion = None
    image = None

    try:

        indice = session_file.rfind("/")
        print(indice)
        if indice != -1:
            log_file = session_file[:indice+1]
            log_file = log_file + "logs.json"
        else:
            print("Erreur : chemin de fichier de session invalide.")
        print(log_file)

        print("logger")
        # Initialiser la variable LOG
        LOG.change_log_file(log_file)
        LOG.change_log_level(DEBUG_LEVEL)
        print("logger ok")

        config: Config = Config.from_config("/home/pi/camtrap/config.json")
        session: Session = Session.from_config(session_file)
        camera = Camera(config)
        lock = Lock()


        if session.choix == "continue" and config:
            log_message_script = {
                "message": "Configuration et session validées."
            }
            LOG.info(log_message_script)
            luminosity = Luminosity(PI_PWM, config.th_jour, config.th_nuit)
            detector = Detector(lock)
            image = Image(camera, detector, config, session, luminosity, lock)

            camera_thread = threading.Thread(target=camera.allumer_camera)
            luminosity_thread = threading.Thread(target=luminosity.brightness_check)

            log_message_script = {
                "message": "Démarrage des threads..."
            }
            LOG.info(log_message_script)

            camera_thread.start()
            luminosity_thread.start()

            camera_thread.join(1)  
            luminosity_thread.join(1)
            
            # print("Appuyez sur Ctrl+C pour arrêter.")

            if not camera_thread.is_alive():
                log_message_script = {
                    "message": "Le thread caméra s'est arrêté. Tentative d'arrêt de luminosité."
                }
                LOG.debug(log_message_script)
                luminosity.stop()
                luminosity = None
            if not luminosity_thread.is_alive():
                log_message_script = {
                    "message": "Le thread luminosité s'est arrêté. Tentative d'arrêt de caméra."
                }
                LOG.debug(log_message_script)
                camera.stop()
            log_message_script = {
                "message": "Threads actifs : caméra et luminosité en cours."
            }
            LOG.info(log_message_script)
            sleep(5)
                


            update_thread = Thread(target=image.update_detector)
            detect_thread = Thread(target=image.detect_movement)
            
            image.start()
            update_thread.start()
            detect_thread.start()
            update_thread.join()
            detect_thread.join()

        if session.choix == "plage" and config:
            log_message_script = {
                "message": "Configuration et session validées."
            }
            LOG.info(log_message_script)

            luminosity = Luminosity(PI_PWM, config.th_jour, config.th_nuit)
            detector = Detector(lock)
            image = Image(camera, detector, config, session, luminosity, lock)

            camera_thread = threading.Thread(target=camera.allumer_camera)
            luminosity_thread = threading.Thread(target=luminosity.brightness_check)

            camera_thread.start()
            luminosity_thread.start()

            camera_thread.join(1)  
            luminosity_thread.join(1)

            if not camera_thread.is_alive():
                log_message_script = {
                    "message": "Le thread caméra s'est arrêté. Tentative d'arrêt de luminosité."
                }
                LOG.debug(log_message_script)
                luminosity.stop()
                luminosity = None
            if not luminosity_thread.is_alive():
                log_message_script = {
                    "message": "Le thread luminosité s'est arrêté. Tentative d'arrêt de caméra."
                }
                LOG.debug(log_message_script)
                camera.stop()
            log_message_script = {
                "message": "Threads actifs : caméra et luminosité en cours."
            }
            LOG.info(log_message_script)
            sleep(5)


            update_thread = Thread(target=image.update_detector)
            detect_thread = Thread(target=image.detect_movement)
            
            update_thread.start()
            detect_thread.start()
            update_thread.join(1)
            detect_thread.join(1) 

            while True:
                maintenant = datetime.now().date()

                log_message_print = {
                    "message": f"aujourd'hui : {maintenant}, début : {session.date_debut}, fin : {session.date_fin}"
                }
                LOG.debug(log_message_print)

                date_debut = datetime.strptime(session.date_debut, '%Y-%m-%d').date()
                date_fin = datetime.strptime(session.date_fin, '%Y-%m-%d').date()
                if date_debut <= maintenant and date_fin >= maintenant:
                    log_message = {
                        "message": "Date de session valide."
                    }
                    LOG.debug(log_message)

                    heure_actuelle = datetime.now().time()
                    log_message = {
                        "message": f"Heure actuelle : {heure_actuelle}"
                    }
                    LOG.debug(log_message)
                    log_message = {
                        "message": f"Plage horaire : {session.time_slots}"
                    }
                    LOG.debug(log_message)

                    start_image = False
                    for slot in session.time_slots:
                        log_message = {
                            "message": f"Slot : {slot}"
                        }
                        LOG.debug(log_message)
                        time_debut = datetime.strptime(slot['time_debut'], '%H:%M').time()
                        time_fin = datetime.strptime(slot['time_fin'], '%H:%M').time()
                        log_message = {
                            "message": f"Slot : {time_debut} - {time_fin}"
                        }
                        LOG.debug(log_message)
                        if time_debut <= heure_actuelle and time_fin > heure_actuelle:
                            log_message = {
                                "message": "Session dans la plage horaire."
                            }
                            LOG.debug(log_message)
                            start_image = True
                            break
                        else:
                            log_message = {
                                "message": "Session en dehors de la plage horaire."
                            }
                            LOG.debug(log_message)
                    print(f"Il est actuellement {heure_actuelle}, start_image = {start_image}.")
                    if start_image:
                        image.start()
                    else:
                        image.pause()
                    sleep(60)
                else:
                    log_message = {
                        "message": "aujourd'hui en dehors de la plage de date."
                    }
                    LOG.debug(log_message)
                    image.pause()
                    sleep(3600)
                
    except KeyboardInterrupt:
        print("\nArrêt manuel du programme.")
        if image:
            image.stop()
        if camera:
            camera.stop()
        if luminosity:
            luminosity.stop()
            luminosity = None

    except Exception as e:
        print(f"Erreur principale : {e}")
    finally:
        print("Nettoyage des ressources...")
        cleanup()

