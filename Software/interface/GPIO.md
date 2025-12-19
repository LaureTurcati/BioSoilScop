# GPIO

##### Mise en place du bouton 

| Couleur du fil  | PIN | Couleur PIN |
|  :---:  |  :----:  |  :---:  |
| Rouge | 3V3 | Orange |
| Blanc | Ground | Noir |
| Noir | GPIO22 | Vert |
___
##### Rédaction du script permettant de passer le raspberry pi en mode wifi ou en mode ap en fonction de la position du bouton
- wifi_ap_gpio.py :
```python
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)  
GPIO_PIN = 22 
GPIO.setup(GPIO_PIN, GPIO.IN) 

def switch_mode(mode):
    if mode == 0:
        print("Switching to WiFi mode")
        subprocess.call(['sudo', '/home/pi/bookworm_wifi_ap_switch.sh', 'wifi'])
    elif mode == 1:
        print("Switching to AP mode")
        subprocess.call(['sudo', '/home/pi/bookworm_wifi_ap_switch.sh', 'ap']) 

try:
    mode = GPIO.input(GPIO_PIN)
    switch_mode(mode)
finally:
    GPIO.cleanup()
```
___
##### Modification des droits 
```bash
sudo chmod +x wifi_ap_gpio.py
sudo chmod +x bookworm_wifi_ap_switch.sh
```
___
##### Lancement du script au boot
```bash
sudo nano /etc/rc.local
```
1. /etc/rc.local :
```
python3 /home/pi/wifi_ap_gpio.py &
```
2. reboot
```bash
sudo reboot
```
3. Voir status :
```bash
systemctl status rc-local
```
4. Voir logs : 
```bash
journalctl -u rc-local
```