import threading, queue, sched
from piball.control.piballevent import PiballEvent


class PiballEventProcessor(threading.Thread):
    def __init__(self, event_queue: queue.Queue, action_scheduler: sched.scheduler, game):
        self.event_queue = event_queue
        self.action_scheduler = action_scheduler
        self.game = game
        threading.Thread.__init__(self)

    def run(self):
        while True:
            event = self.event_queue.get()
            self.process_event(event)

    def process_event(self, event):
        if event is PiballEvent.left_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.game.set_flipper, argument=(0, 1))   # flip up
            self.action_scheduler.enter(0.5, 1, self.game.set_flipper, argument=(0, 0)) # then flip down
        elif event is PiballEvent.right_flipper_button_on:
            self.action_scheduler.enter(0, 1, self.game.set_flipper, argument=(1, 1))   # flip up
            self.action_scheduler.enter(0.5, 1, self.game.set_flipper, argument=(1, 0)) # then flip down