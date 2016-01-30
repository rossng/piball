import time, sched, queue

from piball.control.output import PiballOutputHandler
from piball.game.event_processor import PiballEventProcessor
from piball.game.piball import PiballGame
from piball.serial_comms.mbed import MbedCommunicator
from piball.control.input import PiballInputHandler

#game = PiballGame()

output_pins = {
    'flipper_left_out': 16,
    'flipper_right_out': 18,
    'winding_motor_out': 12,  # PWM
    'plunger_out': 22,
    'mbed_tx': 8,  # UART Tx
    'mbed_rx': 10  # UART Rx
}

input_pins = {
    'flipper_left_button': 11,
    'flipper_right_button': 13,
    'bumper_1': 29,
    'bumper_2': 31,
    'bumper_3': 33,
    'fail': 15
}

output_handler = PiballOutputHandler(output_pins)
event_queue = queue.Queue()
action_scheduler = sched.scheduler(time.time, time.sleep)
game = PiballGame()
event_processor = PiballEventProcessor(event_queue, action_scheduler, game)
input_handler = PiballInputHandler(event_queue, input_pins)