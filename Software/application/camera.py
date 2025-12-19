from picamera2 import Picamera2
from time import sleep
from libcamera import controls
from dataclasses import dataclass

from log import LOG

@dataclass
class Camera:
    def __init__(self, config):
        self.config = config
        self.camera = None
        self.running = True

    def allumer_camera(self):
        try:
            self.camera = Picamera2()
            capture_config = self.camera.create_still_configuration(main={"size": (4608, 2592), "format": "BGR888"}, lores={"size": (640, 480), "format": "YUV420"})
            self.camera.configure(capture_config)
            self.camera.set_controls({
                "Brightness": self.config.brightness,
                "Contrast": self.config.contrast,
                "Saturation": self.config.saturation,
                "AeExposureMode": self.config.exposure,
                "AnalogueGain": self.config.gain,
                "HdrMode": self.config.hdr,
                "AfMode": self.config.autofocus_mode,
                "AfSpeed": self.config.autofocus_speed,
                "AfRange": self.config.autofocus_range
            })
            self.camera.start()
            sleep(2)

            log_message = {"message": "Caméra allumée"}
            LOG.info(log_message)
            print("Thread caméra démarré.")
            while self.running:
                print("Caméra en cours d'exécution...")
                sleep(1)
        except Exception as e:
            print(f"Erreur lors de l'allumage de la caméra : {e}")
            log_message_error = {
                "message": "Erreur avec la caméra",
                "details": str(e),
            }
            LOG.error(log_message_error)
        finally:
            if self.camera:
                self.camera.close()
            print("Caméra arrêtée proprement.")

    def capture_array(self, resolution):
        if resolution == "hires":
            return self.camera.capture_array("main")
        elif resolution == "lores":
            return self.camera.capture_array("lores")
        else:
            return None
        
    def capture_file(self, filepath):
        if not self.camera:
            raise RuntimeError("La caméra n'est pas initialisée. Appelez allumer_camera() d'abord.")
        self.camera.capture_file(filepath)

    def stop(self):
        self.running = False