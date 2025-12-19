import json
from dataclasses import dataclass
from typing import Self

from log import LOG

@dataclass
class Config:
    nom_app: str
    gain :int
    exposure : int
    hdr: int
    brightness: float
    contrast: int
    saturation:float
    autofocus_range:int
    autofocus_mode:int
    autofocus_speed:int
    th_jour: float
    th_nuit: float
    motion_detect_threshold: int
    mov_area: int
    vib_threshold: int
    hq_iteration: int
    interval: float

    @staticmethod
    def from_config(filepath: str) -> Self | None:
        try:
            with open(filepath, "r") as f:
                dataApp = json.load(f)
        except Exception as e:
            print(f"Erreur avec {filepath} :", e)
            log_message_error_app = {
                "message": f"Erreur avec {filepath}",
                "details": str(e)
            }
            LOG.error(log_message_error_app)
            return None

        nom_app = dataApp.get("nom")
        gain = int(dataApp.get("gain", 0))
        exposure = int(dataApp.get("exposure" , 0))
        hdr = int(dataApp.get("hdr", 0))
        brightness = float(dataApp.get("brightness", 0.0))
        contrast = int(dataApp.get("contrast", 0))
        saturation = float(dataApp.get("saturation", 0.0))
        autofocus_range = int(dataApp.get("autofocus-range", 0))
        autofocus_mode = int(dataApp.get("autofocus-mode", 0))
        autofocus_speed = int(dataApp.get("autofocus-speed", 0))
        th_jour = float(dataApp.get("th-jour", 0.0))
        th_nuit = float(dataApp.get("th-nuit", 0.0))
        motion_detect_threshold = int(dataApp.get("motion-detect-threshold", 0))
        mov_area = int(dataApp.get("mov-area", 0))
        vib_threshold = int(dataApp.get("vib-threshold", 0))
        hq_iteration = int(dataApp.get("hq-iteration", 0))
        interval = float(dataApp.get("interval", 0.0))

        log_message_app = {
            "message": "Paramètres de l'application chargés et initialisés",
            "details": dataApp
        }
        print(LOG)
        LOG.info(log_message_app)

        return Config(
            nom_app,
            gain,
            exposure,
            hdr,
            brightness,
            contrast,
            saturation,
            autofocus_range,
            autofocus_mode,
            autofocus_speed,
            th_jour,
            th_nuit,
            motion_detect_threshold,
            mov_area,
            vib_threshold,
            hq_iteration,
            interval
        )
