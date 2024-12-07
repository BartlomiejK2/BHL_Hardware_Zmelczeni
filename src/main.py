import TemperatureSensor as TempSensor
import IMU as ImuSensor
import RPi.GPIO as GPIO

def main():

    # Inicjalizacja systemu 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Inicjalizacja IMU i termometru
    imu_sensor = ImuSensor.IMU(0x68)
    temp_sensor = TempSensor.TemperatureSensor()
    