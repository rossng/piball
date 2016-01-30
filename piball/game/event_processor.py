import threading, queue, sched

from piball.control.output import PiballOutputHandler
from piball.control.piballevent import PiballEvent
from piball.game.piball import PiballGame


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
        if event is PiballEvent.left_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_flipper, argument=(0, 1))   # flip up
            self.action_scheduler.enter(0.5, 1, self.output_handler.set_flipper, argument=(0, 0)) # then flip down
            self.action_scheduler.enter(0, 2, self.game.increment_score)
        elif event is PiballEvent.right_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.output_handler.set_flipper, argument=(1, 1))   # flip up
            self.action_scheduler.enter(0.5, 1, self.output_handler.set_flipper, argument=(1, 0)) # then flip down
            self.action_scheduler.enter(0, 2, self.game.increment_score)