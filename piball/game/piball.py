from piball.control.output import PiballOutputHandler
from enum import Enum

class GameEvent(Enum):
    ball_in_play = 1


class PiballGame:
    score = 0
    lives = 0
    balls_in_play = 0

    def __init__(self, output_handler: PiballOutputHandler):
        self.output_handler = output_handler
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = 3
        print('GAME: new game')

    def increment_score(self):
        self.score += 1
        print('GAME: score ' + str(self.score))

    def ball_out(self):
        self.lose_life()

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.reset()
