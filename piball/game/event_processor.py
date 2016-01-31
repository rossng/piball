import threading, queue, sched

from piball.control.output import PiballOutputHandler
from piball.control.piball_event import PiballEvent
from piball.game.piball import PiballGame
from piball.serial_comms.mbed_modes import MbedMode


class PiballEventProcessor(threading.Thread):
    def __init__(self, event_queue: queue.Queue, action_scheduler: sched.scheduler,
                 game: PiballGame, output_handler: PiballOutputHandler):
        self.event_queue = event_queue
        self.action_scheduler = action_scheduler
        self.game = game
        self.output_handler = output_handler
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.action_scheduler.run(blocking=False)
            try:
                event = self.event_queue.get_nowait()
                print('EVP: Processing event ' + str(event))
                self.process_event(event)
            except queue.Empty:
                continue

    def process_event(self, event):
        # when the user presses the left flipper button
        if event is PiballEvent.left_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_flipper, argument=(0, 1))      # flip up
            self.action_scheduler.enter(0.5, 1, self.output_handler.set_flipper, argument=(0, 0))    # then flip down

        # when the user presses the right flipper button
        elif event is PiballEvent.right_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_flipper, argument=(1, 1))    # flip up
            self.action_scheduler.enter(0.5, 1, self.output_handler.set_flipper, argument=(1, 0))  # then flip down

        # when the ball goes out
        elif event is PiballEvent.fail_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_winding_motor, argument=(1,))  # pull back elastic
            self.action_scheduler.enter(5, 1, self.output_handler.set_winding_motor, argument=(0,))  # stop pulling
            self.action_scheduler.enter(0, 1, self.game.ball_out)                                    # notify game that ball is out

        # when the user presses the auto-plunge button
        elif event is PiballEvent.plunger_button_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_plunger_pin, argument=(1,))   # hold pin down
            self.action_scheduler.enter(0, 1, self.output_handler.set_winding_motor, argument=(2,)) # loosen elastic hold
            self.action_scheduler.enter(3, 1, self.output_handler.set_winding_motor, argument=(0,)) # stop loosening
            self.action_scheduler.enter(4, 1, self.output_handler.set_plunger_pin, argument=(0,))   # release pin
            self.action_scheduler.enter(4, 1, self.game.ball_fired)                                 # notify game that ball fired

        # when the ball rolls onto a bumper
        elif event is PiballEvent.bumper_1_on or event is PiballEvent.bumper_2_on or event is PiballEvent.bumper_3_on:
            self.action_scheduler.enter(0, 1, self.game.increment_score, argument=(20,))

        # when the ball rolls across the neopixel pad
        elif event is PiballEvent.pad_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_neopixel_mode, argument=(MbedMode.colourful,))
            self.action_scheduler.enter(5, 1, self.output_handler.set_neopixel_mode, argument=(MbedMode.normal,))
            self.action_scheduler.enter(0, 1, self.game.increment_score, argument=(50,))
            self.action_scheduler.enter(0, 1, self.game.update_score_multiplier, argument=(2,))

        elif event is PiballEvent.game_over:
            self.action_scheduler.enter(0, 1, self.output_handler.set_neopixel_mode, argument=(MbedMode.dead,))

