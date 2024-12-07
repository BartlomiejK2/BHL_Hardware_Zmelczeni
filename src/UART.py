import serial



class UART:

    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, 9600)
        self.data_string = None
        try:
            self.serial.open()
        except:
            print("UART nie działa stupid!")


    def read_message(self):
        if(self.data_string is not None):
            print("Jakies dane sa juz w buforze, wez je!")
            return
        data = self.serial.readline()
        self.data_string = str(data, encoding='utf-8')
        self.data_string.strip("\n")

    def get_message(self):
        if(self.data_string is None):
            print("Nie dostales zadnej wiadomosci, najpierw cos odbierz!")
        type = self.__check_message_type()
        value = int("0x" + self.data_string, 0)
        self.data_string = None
        return {type: value}

    def __check_message_type(self):
        if(self.data_string is None):
            print("Nie dostales zadnej wiadomosci, najpierw cos odbierz!")
        message_type = self.data_string[0]
        del self.data_string[0]
        if(message_type == "g"):
            return "GAS"
        elif(message_type == "h"):
            return "HEART"
        
    