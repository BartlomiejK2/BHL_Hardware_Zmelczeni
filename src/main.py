#import TemperatureSensor as TempSensor
import IMU 
import RPi.GPIO as GPIO
import UART
import threading
import queue
import time

IMU_SLEEP_TIME = 0.001
UART_SLEEP_TIME = 0.01

def ImuThread(IMU: IMU.IMU, accel_queue: queue.Queue, orient_queue: queue.Queue, temp_queue: queue.Queue):
    while True:
        data = IMU.get_data()
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
    imu_sensor = IMU.IMU(0x68)
    #temp_sensor = TempSensor.TemperatureSensor()
    #uart = UART.UART(PORT)

    # Kolejki dla danych z czujników
    acceleration = queue.Queue(1)
    orientation = queue.Queue(1)
    temperature = queue.Queue(1)
    pulse = queue.Queue(1)
    gas = queue.Queue(1)

    # Wątki dla czujników
    imu_thread = threading.Thread(target = ImuThread, args = (imu_sensor, acceleration, orientation, temperature))
    #uart_thread = threading.Thread(target = UartThread, args = (uart, pulse, gas))

    imu_thread.start()
    #uart_thread.start()

    # Głowny thread:
    orientation_string = ""
    acceleration_string = ""
    temperature_string = ""
    while True:
        if(orientation.full()):
            orientation_string = f"ORIENTACJA: {orientation.get()}\n"
        if(acceleration.full()):
            acceleration_string = f"ACCELERATION: {acceleration.get()}\n"
        if(temperature.full()):
            temperature_string = f"TEMPERATURE: {temperature.get()}"
        print(orientation_string + acceleration_string + temperature_string, flush = True)

    imu_thread.join()
    #uart_thread.join()

    uart.close()


    
main()