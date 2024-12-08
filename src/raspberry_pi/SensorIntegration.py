from EmotionRecognition import EmotionRecognition
from UART import UART
from IMU import IMU, Acceleration, Orientation
from math import sqrt
class SensorIntegration:
    
    def __init__(self):
        self.temperature = None
        self.acceleration = None
        self.orientation = None
        self.pulse = None
        self.gas = None
        self.emotion = None

        self.MAX_TEMPERATURE = 45
        self.MIN_TEMPERATURE = 0

        self.MAX_ACCELERATION = 3 * 9.81

        self.MIN_PULSE = 25.0

        self.MAX_GAS = 10.0

        self.MAX_ORIENTATION = 120
    
    def update_data(self, emotion, acceleration, orientation, pulse, gas, temperature):
        self.emotion = emotion
        self.acceleration = acceleration
        self.orientation = orientation
        self.pulse = pulse
        self.gas = gas
        self.temperature = temperature

    def check_temperature(self):
        if(self.temperature is None): return None
        return self.temperature < self.MAX_TEMPERATURE and self.temperature > self.MIN_TEMPERATURE
    
    def check_acceleration(self):
        if(self.acceleration is None): return None
        acceleration = sqrt(self.acceleration.x**2 + self.acceleration.y**2 + self.acceleration.z**2)
        return acceleration < self.MAX_ACCELERATION
    
    def check_pulse(self):
        if(self.pulse is None): return None
        return self.pulse > self.MIN_PULSE
    
    def check_gas(self):
        if(self.gas is None): return None
        return self.gas < self.MAX_GAS
    
    def check_orientation(self):
        if(self.orientation is None): return None
        x = self.orientation.x < self.MAX_ORIENTATION and self.orientation.x > -self.MAX_ORIENTATION
        y = self.orientation.y < self.MAX_ORIENTATION and self.orientation.y > -self.MAX_ORIENTATION
        return x and y
    
    def integrate(self):
        return