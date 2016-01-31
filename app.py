import time, sched, queue

from piball.control.output import PiballOutputHandler
from piball.game.event_processor import PiballEventProcessor
from piball.game.piball import PiballGame
from piball.control.input import PiballInputHandler


output_pins = {
    'flipper_left': 16,
    'flipper_right': 18,
    'winding_motor': 12,  # PWM
    'plunger_pin': 22,
    'mbed_tx': 8,  # UART Tx
    'mbed_rx': 10  # UART Rx
}

input_pins = {
    'flipper_left_button': 11,
    'flipper_right_button': 13,
    'bumper_1': 29,
    'bumper_2': 31,
    'bumper_3': 33,
    'fail': 15,
    'plunger_button': 24
}

event_queue = queue.Queue()
action_scheduler = sched.scheduler(time.time, time.sleep)
output_handler = PiballOutputHandler(output_pins)
game = PiballGame(output_handler)
event_processor = PiballEventProcessor(event_queue, action_scheduler, game, output_handler)
input_handler = PiballInputHandler(event_queue, input_pins)
event_processor.start()
event_processor.join()