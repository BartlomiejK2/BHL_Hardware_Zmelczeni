import serial

class UART:

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600)
        self.data = None
        self.gas_value = None
        self.pulse_value = None


    def get_message(self):
        data = self.serial.readline()
        iter = 0
        if(len(data) < 11):
            return 
        while iter < len(data):
            pulse_data = bytearray()
            gas_data = bytearray()
            if(data[iter] == int.from_bytes(b'h')):
                iter += 1
                while data[iter] is not int.from_bytes(b'g'):
                    pulse_data.append(data[iter])
                    iter += 1
                iter += 1
                while data[iter] is not int.from_bytes(b"\n"):
                    gas_data.append(data[iter])
                    iter += 1                             
                self.pulse_value = float(pulse_data.decode("utf-8"))
                self.gas_value = float(gas_data.decode("utf-8"))
            iter += 1
        return [self.pulse_value, self.gas_value]
    def close(self):
        self.serial.close()
    