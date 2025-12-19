# **Guide des paramètres pour la PiCam 3**

Ce document fournit une explication détaillée des paramètres utilisés pour CamTrap via Python et la bibliothèque `picamera2`. Vous trouverez ici des descriptions, des plages de valeurs, et des exemples pratiques pour optimiser vos réglages.

___
## **1. Paramètres généraux**

### `AnalogueGain` (Gain analogique)
- **Description** : Contrôle la sensibilité du capteur à la lumière.
- **Plage de valeurs** : `1.0` (par défaut) à `16.0`.
- **Notes** : 
  - Un gain élevé améliore la luminosité en basse lumière, mais introduit du bruit.

___
### `HdrMode` (Mode HDR)
- **Description** : Active ou ajuste le HDR (High Dynamic Range) pour capturer des détails dans les ombres et les hautes lumières.
- **Modes disponibles** :
  - `0` : Désactivé (par défaut).
  - `1` : Faible HDR.
  - `2` : HDR moyen.
  - `3` : HDR élevé.
  - `4` : Automatique.

___
### `Brightness` (Luminosité)
- **Description** : Ajuste la luminosité globale de l'image.
- **Plage de valeurs** : `-1.0` (minimum) à `1.0` (maximum), `0.0` par défaut.

___
### `Contrast` (Contraste)
- **Description** : Modifie la différence entre les zones sombres et lumineuses.
- **Plage de valeurs** : `0.0` (faible) à `32.0` (élevé), `1.0` par défaut.

___
### `Saturation` (Saturation des couleurs)
- **Description** : Ajuste l'intensité des couleurs dans l'image.
- **Plage de valeurs** : `0.0` (niveaux de gris) à `32.0` (très saturé), `1.0` par défaut.

___
### `Sharpness` (Netteté)
- **Description** : Ajuste la netteté de l'image.
- **Plage de valeurs** : `0.0` (aucune netteté) à `16.0` (très net), `1.0` par défaut.

___
## **2. Paramètres de mise au point**

### `AfMode` (Mode autofocus)
- **Description** : Définit le mode de mise au point automatique.
- **Modes disponibles** :
  - `0` : Auto (par défaut).
  - `1` : Continuous (mise au point continue).

___
### `AfRange` (Plage de mise au point)
- **Description** : Limite la plage de distances pour la mise au point.
- **Modes disponibles** :
  - `0` : Normal (standard).
  - `1` : Macro (proche).
  - `2` : Full (complète).

___
### `AfSpeed` (Vitesse de mise au point)
- **Description** : Contrôle la rapidité de la mise au point.
- **Modes disponibles** :
  - `0` : Normal (équilibré).
  - `1` : Rapide (moins précis).

___
## **3. Paramètre avancé**

### `AeExposureMode` (Mode d'exposition automatique)
- **Description** : Gère automatiquement l'exposition selon la scène.
- **Modes disponibles** :
  - `0` : Auto (par défaut).
  - `1` : Night (faible lumière).
  - `2` : Backlight (contre-jour).
  - `3` : Spotlight (projecteurs).

___
## **4. Exemple d'utilisation avec Python**

```python
from picamera2 import Picamera2
from libcamera import controls

# Initialisation de la caméra
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)

# Réglages des paramètres
picam2.set_controls({
    "AnalogueGain": 2.0,
    "AeExposureMode": 0,
    "HdrMode": 3,  # HDR élevé
    "Brightness": 0.5,
    "Contrast": 1.5,
    "Saturation": 1.2,
    "AfMode": 1,  # Autofocus continu
    "AfSpeed": 0,  # Vitesse normale
})

# Démarrage de la capture
picam2.start_preview()
picam2.start()

# Capture d'une image
picam2.capture_file("image.jpg")

# Arrêt de la caméra
picam2.stop()

```
