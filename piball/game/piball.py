from queue import Queue

from piball.control.output import PiballOutputHandler
from enum import Enum

from piball.control.piball_event import PiballEvent


class GameEvent(Enum):
    ball_in_play = 1


class PiballGame:
    score = 0                       # what is the user's current score?
    lives = 0                       # how many lives does the user have?
    ball_in_play = False            # is there a ball in play?
    super_score_mode = False        # is the user currently in double-scoring mode?

    def __init__(self, output_handler: PiballOutputHandler, event_queue: Queue):
        self.output_handler = output_handler
        self.event_queue = event_queue
        self.reset()

    def reset(self):
        self.ball_in_play = False
        self.score = 0
        self.lives = 3
        print('GAME: new game')

    def increment_score(self, by=1):
        self.score += 1 * (2 if self.super_score_mode else 1)
        print('GAME: score ' + str(self.score))

    def ball_fired(self):
        self.ball_in_play = True

    def ball_out(self):
        if self.ball_in_play:
            self.lose_life()
        self.ball_in_play = False

    def bumper_hit(self):
        self.increment_score(by=20)

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.event_queue.put(PiballEvent.game_over)
            self.reset()
