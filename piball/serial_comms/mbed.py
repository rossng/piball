import serial, io


class MbedCommunicator:
    def __init__(self, baudrate=115200, timeout=3.0):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=baudrate, timeout=timeout)

    def send_command(self, command_text):
        command = command_text + '\n'
        self.port.write(command.encode('latin-1'))
        print('MBED: Sent serial command')
        maybe_ack = self.port.readline()
        if maybe_ack == 'ack\n':
            print('MBED: Command sent successfully')
        else:
            print('MBED: Command was not acknowledged')