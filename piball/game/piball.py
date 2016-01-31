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
    score_multiplier = 1            # is the user currently in double-scoring mode?
    def __init__(self, output_handler: PiballOutputHandler, event_queue: Queue, socket):
        self.output_handler = output_handler
        self.event_queue = event_queue
        self.user = -1
        self.playing = 1
        self.socket = socket
        self.ball_in_play = False
        self.reset()

    def start_game(self, user):
        self.user = user
        self.score = 0
        self.playing = 1

    def reset(self):
        self.ball_in_play = False
        self.score = 0
        self.playing = 0
        self.user = -1
        self.lives = 3
        self.score_multiplier = 1
        print('GAME: new game')

    def increment_score(self, by=1):
        self.score += 1 * self.score_multiplier
        self.socket.emit('currentGame' , self.tojson()  , room = 'play' )
        print('GAME: score ' + str(self.score))

    def  tojson(self):
        json = {}
        json["score"] = self.score
        json["playing"] =  self.playing
        json["user"] = self.user
        return json
    def ball_fired(self):
        self.ball_in_play = True

    def ball_out(self):
        if self.ball_in_play:
            self.lose_life()
        self.ball_in_play = False
        self.score_multiplier = 1

    def update_score_multiplier(self, factor: float):
        self.score_multiplier *= factor
        print('GAME: score multiplier ' + str(self.score_multiplier))

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.event_queue.put(PiballEvent.game_over)
            self.reset()
