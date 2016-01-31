import threading

import serial, io, queue

from piball.serial_comms.mbed_modes import MbedMode


class MbedCommunicator(threading.Thread):
    mode_map = {MbedMode.normal: b'b', MbedMode.colourful: b'a'}

    def __init__(self, baudrate=115200):
        self.port = serial.Serial("/dev/ttyAMA0", baudrate=baudrate)
        self.command_queue = queue.Queue()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                command = self.command_queue.get_nowait()
                print('EVP: Processing command ' + str(command))
                self.send_command(command)
            except queue.Empty:
                continue

    def send_command(self, mode: MbedMode):
        self.port.write(b's')
        self.port.write(self.mode_map[mode])
        print('MBED: Sent serial command ' + str(mode))
