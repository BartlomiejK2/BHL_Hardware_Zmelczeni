import mpu6050
from dataclasses import dataclass

@dataclass
class Acceleration:
    x: float
    y: float
    z: float

@dataclass
class Orientation:
    x: float
    y: float
    z: float

class IMU:
    def __init__(self, address, time_delta):
        self.time_delta = time_delta
        self.orientation = Orientation(0,0,0)
        self.sensor = mpu6050.mpu6050(address)
        self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
        self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
        self.sensor.set_filter_range()

    def get_acceleration(self):
        accel_data = self.sensor.get_accel_data(g = False)
        acceleration = Acceleration(accel_data["x"], accel_data["y"], accel_data["z"])
        return acceleration
    
    def get_temperature(self):
        return self.sensor.get_temp()
    
    def get_orientation(self):
        gyro_data = self.sensor.get_gyro_data()
        dx = gyro_data["x"] * self.time_delta
        dy = gyro_data["y"] * self.time_delta
        dz = gyro_data["z"] * self.time_delta
        self.orientation.x += dx
        self.orientation.y += dy
        self.orientation.z += dz 
        return self.orientation