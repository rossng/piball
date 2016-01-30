import RPi.GPIO as GPIO

from piball.serial_comms.mbed import MbedCommunicator


class PiballOutputHandler:
    def flipper_left_up(self):
        GPIO.output(self.pins['flipper_left_out'], GPIO.HIGH)

    def flipper_left_down(self):
        GPIO.output(self.pins['flipper_left_out'], GPIO.LOW)

    def flipper_right_up(self):
        GPIO.output(self.pins['flipper_right_out'], GPIO.HIGH)

    def flipper_right_down(self):
        GPIO.output(self.pins['flipper_right_out'], GPIO.LOW)

    def __init__(self, output_pins):
        self.pins = output_pins
        self.mbed = MbedCommunicator()
        self.mbed.send_command("hello")
        GPIO.setmode(GPIO.BOARD)