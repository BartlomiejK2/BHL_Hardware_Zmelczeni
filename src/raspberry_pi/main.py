#import TemperatureSensor as TempSensor
from IMU import IMU, Acceleration, Orientation 
import RPi.GPIO as GPIO
import UART
import threading
import queue
import time

IMU_SLEEP_TIME = 0.001
UART_SLEEP_TIME = 0.01

def ImuThread(IMU: IMU, accel_queue: queue.Queue, orient_queue: queue.Queue, temp_queue: queue.Queue):
    while True:
        data = IMU.get_data()
        if(data[0] == Acceleration(0, 0, 0) and data[1] == Orientation(0, 0, 0)):
            time.sleep(IMU_SLEEP_TIME)
            continue

        if(accel_queue.full()):
           accel_queue.get()
        accel_queue.put(data[0])

        if(orient_queue.full()):
            orient_queue.get()
        orient_queue.put(data[1])

        if(temp_queue.full()):
            temp_queue.get()
        temp_queue.put(data[2])
        
        time.sleep(IMU_SLEEP_TIME)

def UartThread(uart: UART.UART, pulse_queue: queue.Queue, gas_queue: queue.Queue):
    while True:
        message = uart.get_message()
        if message == None:
            time.sleep(1)
            continue
        if(gas_queue.full()):
            gas_queue.get()
        gas_queue.put(message[0])
        if(pulse_queue.full()):
            pulse_queue.get()
        pulse_queue.put(message[1])
        time.sleep(UART_SLEEP_TIME)


# TODO
PORT = "/dev/ttyUSB0"

def main():

    # Inicjalizacja systemu 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Inicjalizacja IMU, termometru i UART'a
    imu_sensor = IMU(0x68)
    #temp_sensor = TempSensor.TemperatureSensor()
    uart = UART.UART(PORT)

    # Kolejki dla danych z czujników
    acceleration = queue.Queue(1)
    orientation = queue.Queue(1)
    temperature = queue.Queue(1)
    pulse = queue.Queue(1)
    gas = queue.Queue(1)

    # Wątki dla czujników
    imu_thread = threading.Thread(target = ImuThread, args = (imu_sensor, acceleration, orientation, temperature))
    uart_thread = threading.Thread(target = UartThread, args = (uart, pulse, gas))

    imu_thread.start()
    uart_thread.start()

    # Głowny thread:
    orientation_string = ""
    acceleration_string = ""
    temperature_string = ""
    pulse_string = ""
    gas_string = ""
    while True:
        if(orientation.full()):
            orientation_string = f"ORIENTACJA: {orientation.get()}\n"
        if(acceleration.full()):
            acceleration_string = f"ACCELERATION: {acceleration.get()}\n"
        if(temperature.full()):
            temperature_string = f"TEMPERATURE: {temperature.get()}\n"
        if(pulse.full()):
            pulse_string = f"PULSE: {pulse.get()}\n"
        if(gas.full()):
            gas_string = f"GAS: {gas.get()}\n"
        print(orientation_string + acceleration_string + temperature_string +
              pulse_string + gas_string, flush = True)

    imu_thread.join()
    uart_thread.join()

    uart.close()


    
main()