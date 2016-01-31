import queue

from piball.control.piball_event import PiballEvent

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO")


class PiballInputHandler:

    def register_pin(self, pin, edge, callback):
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, edge, callback=callback, bouncetime=400)

    def left_flipper_button_on(self, channel):
        print('INPUT: Left flipper on')
        self.event_queue.put(PiballEvent.left_flipper_button_on)

    def right_flipper_button_on(self, channel):
        print('INPUT: Right flipper on')
        self.event_queue.put(PiballEvent.right_flipper_button_on)

    def left_flipper_button_off(self, channel):
        print('INPUT: Left flipper off')
        self.event_queue.put(PiballEvent.left_flipper_button_off)

    def right_flipper_button_off(self, channel):
        print('INPUT: Right flipper off')
        self.event_queue.put(PiballEvent.right_flipper_button_off)

    def fail(self, channel):
        print('INPUT: Fail')
        self.event_queue.put(PiballEvent.fail_on)

    def pad(self, channel):
        print('INPUT: Pad')
        self.event_queue.put(PiballEvent.pad_on)

    def bumper_1(self, channel):
        print('INPUT: Bumper 1')
        self.event_queue.put(PiballEvent.bumper_1_on)

    def bumper_2(self, channel):
        print('INPUT: Bumper 2')
        self.event_queue.put(PiballEvent.bumper_2_on)

    def bumper_3(self, channel):
        print('INPUT: Bumper 3')
        self.event_queue.put(PiballEvent.bumper_3_on)

    def __init__(self, queue: queue.Queue, input_pins):
        self.pins = input_pins
        self.event_queue = queue
        GPIO.setmode(GPIO.BOARD)

        # TODO find a way to handle GPIO.BOTH nicely

        self.register_pin(self.pins.get('flipper_left_button'), GPIO.RISING, self.left_flipper_button_on)
        #self.register_pin(self.pins.get('flipper_left_button'), GPIO.FALLING, self.left_flipper_button_off)
        self.register_pin(self.pins.get('flipper_right_button'), GPIO.RISING, self.right_flipper_button_on)
        #self.register_pin(self.pins.get('flipper_right_button'), GPIO.FALLING, self.right_flipper_button_off)
        self.register_pin(self.pins.get('fail'), GPIO.RISING, self.fail)
        self.register_pin(self.pins.get('bumper_1'), GPIO.RISING, self.bumper_1)
        self.register_pin(self.pins.get('bumper_2'), GPIO.RISING, self.bumper_1)
        self.register_pin(self.pins.get('bumper_3'), GPIO.RISING, self.bumper_1)
        self.register_pin(self.pins.get('pad'), GPIO.RISING, self.pad)
