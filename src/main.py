#import TemperatureSensor as TempSensor
import IMU 
import RPi.GPIO as GPIO
import UART
import threading
import queue
import time

IMU_SLEEP_TIME = 0.01
UART_SLEEP_TIME = 0.01

def ImuThread(IMU: IMU.IMU, accel_queue: queue.Queue, orient_queue: queue.Queue):
    while True:
        if(accel_queue.full()):
           accel_queue.get()
        accel_queue.put(IMU.get_acceleration())   
        if(orient_queue.full()):
            orient_queue.get()
        orient_queue.put(IMU.get_orientation())
        time.sleep(IMU_SLEEP_TIME)

def UartThread(uart: UART.UART, pulse_queue: queue.Queue, gas_queue: queue.Queue):
    while True:
        uart.read_message()
        message = uart.get_message()
        type = message.keys()[0]
        value = message.values()[0]

        if(type == "GAS"):
            if(gas_queue.full()):
                gas_queue.get()
            gas_queue.put(value)

        elif(type == "HEART"):
            if(pulse_queue.full()):
                pulse_queue.get()
            pulse_queue.put(value)
        time.sleep(UART_SLEEP_TIME)


# TODO
PORT = "/dev/ttyUSB0"

def main():

    # Inicjalizacja systemu 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Inicjalizacja IMU, termometru i UART'a
    imu_sensor = IMU.IMU(0x68, IMU_SLEEP_TIME)
    #temp_sensor = TempSensor.TemperatureSensor()
    #uart = UART.UART(PORT)

    # Kolejki dla danych z czujników
    acceleration = queue.Queue(1)
    orientation = queue.Queue(1)
    pulse = queue.Queue(1)
    gas = queue.Queue(1)

    # Wątki dla czujników
    imu_thread = threading.Thread(target = ImuThread, args = (imu_sensor, acceleration, orientation))
    #uart_thread = threading.Thread(target = UartThread, args = (uart, pulse, gas))

    imu_thread.start()
    #uart_thread.start()

    # Głowny thread:
    while True:
        if(orientation.full()):
            print(f"ORIENTACJA: {orientation.get()}")
        if(acceleration.full()):
            print(f"ACCELERATION: {acceleration.get()}")
    

    imu_thread.join()
    #uart_thread.join()

    uart.close()


    
main()