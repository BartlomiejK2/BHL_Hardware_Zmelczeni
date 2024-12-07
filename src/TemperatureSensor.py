import time
import RPi.GPIO as GPIO
import w1thermsensor


class TemperatureSensor():
    def __init__(self):
        self.sensor = w1thermsensor.W1ThermSensor()

    def get_temp_temperatur(self):
        return self.sensor.get_temperature()
