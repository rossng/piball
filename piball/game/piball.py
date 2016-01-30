from piball.control.controller import PiballController
import time, sched

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")


class PiballGame:
    def __init__(self):
        controller = PiballController()

    def button_pressed(self, channel):
        print('Button pressed on channel %s' % channel)

    def play(self):
        GPIO.setup(12, GPIO.IN)
        GPIO.add_event_detect(12, GPIO.RISING, callback=self.button_pressed)
