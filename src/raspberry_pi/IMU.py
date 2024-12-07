import mpu6050
from dataclasses import dataclass
from time import time

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
    def __init__(self, address):
        self.previous_time = time()
        self.calibrated = False
        self.iteration = 1
        self.orientation = Orientation(0,0,0)
        self.acceleration = Acceleration(0, 0, 0)
        self.orientation_error = Orientation(0, 0, 0)
        self.acceleration_error = Acceleration(0, 0, 0)
        self.sensor = mpu6050.mpu6050(address)
        self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_8G)
        self.sensor.set_gyro_range(self.sensor.GYRO_RANGE_250DEG)
        self.sensor.set_filter_range()

    def get_acceleration(self):
        accel_data = self.sensor.get_accel_data(g = False)

        accel_x = accel_data["x"]
        accel_y = accel_data["y"]
        accel_z = accel_data["z"]
        if not self.calibrated:
            self.acceleration_error.x += accel_x
            self.acceleration_error.y += accel_z
            self.acceleration_error.z += accel_y
        else:
            self.acceleration.x = accel_x - self.acceleration_error.x / self.iteration
            self.acceleration.y = accel_y - self.acceleration_error.y / self.iteration
            self.acceleration.z = accel_z - self.acceleration_error.z / self.iteration

        return self.acceleration
    
    def get_temperature(self):
        return self.sensor.get_temp()
    
    def get_orientation(self, delta_time):
        gyro_data = self.sensor.get_gyro_data()
        dx = gyro_data["x"] * delta_time
        dy = gyro_data["y"] * delta_time
        dz = gyro_data["z"] * delta_time
        if not self.calibrated:
            self.orientation_error.x += dx
            self.orientation_error.y += dy
            self.orientation_error.z += dz
        else:
            self.orientation.x += dx - self.orientation_error.x / self.iteration
            self.orientation.y += dy - self.orientation_error.y / self.iteration
            self.orientation.z += dz - self.orientation_error.z / self.iteration
        return self.orientation
    
    def get_data(self):
        current_time = time()
        delta_time = current_time - self.previous_time
        #print(f"Delta time: {delta_time}")
        self.previous_time = current_time
        if not self.calibrated:
            if self.iteration == 1000:
                self.calibrated = True
            self.iteration += 1
        acceleration = self.get_acceleration()
        orientation = self.get_orientation(delta_time)
        temperature = self.get_temperature()
        return [acceleration, orientation, temperature]