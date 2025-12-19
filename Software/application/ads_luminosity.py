import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def detect_luminosity():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    channel = AnalogIn(ads, ADS.P0)

    voltage = channel.voltage

    return voltage

if __name__ == "__main__":
    try:
        luminosity = detect_luminosity()
        print(f"{luminosity:.2f}")
    except Exception as e:
        print(f"Erreur : {e}")
