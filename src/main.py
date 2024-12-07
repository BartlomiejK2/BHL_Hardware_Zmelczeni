import TemperatureSensor as TempSensor
import RPi.GPIO as GPIO

def main():

    # Inicjalizacja systemu 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)