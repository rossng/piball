from piball.control.output import PiballOutputHandler
from enum import Enum

class GameEvent(Enum):
    ball_in_play = 1


class PiballGame:
    def __init__(self, output_handler: PiballOutputHandler, socket):
        self.output_handler = output_handler
        self.score = 0
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
        print('GAME: new game')

    def increment_score(self):
        self.score += 1
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

    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.reset()
