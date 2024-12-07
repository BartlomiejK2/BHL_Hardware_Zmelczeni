import TemperatureSensor as TempSensor
import IMU as ImuSensor
import RPi.GPIO as GPIO
import UART

# TODO
class ImuThread:
    def __init__(self, lock):
        self.lock = lock

# TODO
PORT = "/dev/ttyUSB0"

def main():

    # Inicjalizacja systemu 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Inicjalizacja IMU, termometru i UART'a
    imu_sensor = ImuSensor.IMU(0x68)
    temp_sensor = TempSensor.TemperatureSensor()
    uart = UART.UART(PORT)

    #Inicjalizacja danych z IMU, termometru i UART'a
    acceleration = ImuSensor.Acceleration()
    orientation = ImuSensor.Orientation()
    pulse = 0
    gas = 0

    
