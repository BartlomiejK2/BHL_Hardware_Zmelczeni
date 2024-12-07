import TemperatureSensor as TempSensor
import RPi._GPIO as GPIO

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)