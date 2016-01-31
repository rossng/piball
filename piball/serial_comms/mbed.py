import serial, io


class MbedCommunicator:
    def __init__(self, baudrate=115200, timeout=3.0):
        self.port = serial.Serial("/dev/ttyUSB0", baudrate=baudrate, timeout=timeout)

    def send_command(self, char):
        self.port.write('\x02'.encode('latin-1'))
        self.port.write(char.encode('latin-1'))
        print('MBED: Sent serial command')
        maybe_ack = self.port.readline()
        if maybe_ack == '\x06':
            print('MBED: Command sent successfully')
        else:
            print('MBED: Command was not acknowledged')