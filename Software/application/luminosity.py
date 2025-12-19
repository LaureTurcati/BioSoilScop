import subprocess
from time import sleep

from log import LOG

class Luminosity:
    def __init__(self, pwm, th_jour, th_nuit):
        self.pwm = pwm
        self.running = True
        self.env_activated = False
        self.th_jour = th_jour
        self.th_nuit = th_nuit

    def get_luminosity(self) -> float | None:
        try:
            command = f" /home/pi/ads1115/bin/python3 /home/pi/app/ads_luminosity.py"
            result = subprocess.check_output(command, shell=True, text=True).strip()
            luminosity = float(result)

            log_message_luminosity = {
                "message": f"Luminosité mesurée : {luminosity:.2f} V",
            }
            LOG.debug(log_message_luminosity)
            return luminosity
        except ValueError:
            log_message_luminosity = {
                "message": f"Valeur inattendue retournée par le script : {result}"
            }
            LOG.error(log_message_luminosity)
            return None

        except Exception as e:
            log_message_luminosity = {
                "message": f"Erreur lors de la détection de luminosité : {e}"
            }
            LOG.error(log_message_luminosity)
            return None
        
    def get_mode(self, current_value) -> str | None:
        result = None
        if luminosity_value := self.get_luminosity():
            result = current_value
            if  current_value == "jour" and luminosity_value >= self.th_nuit:
                result = "nuit"
            elif current_value == "nuit" and luminosity_value <= self.th_jour:
                result = "jour" 
            elif current_value == None:
                if luminosity_value >= self.th_nuit:
                    result = "nuit"
                else:
                    result = "jour"
                
        return result

    def brightness_check(self):
        log_message_luminosity = {"message": "Démarrage de la vérification de luminosité."}
        LOG.info(log_message_luminosity)
        while self.running:
            try:
                luminosity = self.get_luminosity()
                if luminosity is not None:
                    duty = luminosity * 100 - 100
                    if duty > 100:
                        duty = 100
                    elif duty < 0:
                        duty = 0
                    self.pwm.ChangeDutyCycle(duty)
                sleep(1)
            except Exception as e:
                log_message_luminosity = {"message": f"Erreur dans brightness_check : {e}"}
                LOG.error(log_message_luminosity)

    def stop(self):
        log_message_luminosity = {"message": "Arrêt du processus de vérification de luminosité."}
        LOG.info(log_message_luminosity)
        self.running = False
