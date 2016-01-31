import RPi.GPIO as GPIO
from typing import Mapping

from piball.serial_comms.mbed import MbedCommunicator


class PiballOutputHandler:
    def set_flipper(self, id, pos):
        print('OUT: setting flipper ' + str(id) + ' to ' + str(pos))
        pos = GPIO.HIGH if pos == 1 else GPIO.LOW
        if id == 0:
            GPIO.output(self.pins['flipper_left_out'], pos)
        elif id == 1:
            GPIO.output(self.pins['flipper_right_out'], pos)

    def __init__(self, output_pins: Mapping[str, int] ):
        self.pins = output_pins
        self.mbed = MbedCommunicator()
        self.mbed.send_command("hello")
        GPIO.setmode(GPIO.BOARD)

        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)