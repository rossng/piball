from piball.control.output import PiballOutputHandler


class PiballGame:
    def __init__(self, output_handler: PiballOutputHandler , socket):
        self.output_handler = output_handler
        self.score = 0
        self.user = -1
        self.playing = 1
        self.socket = socket
        self.reset()

    def start_game(self, user):
        self.user = user
        self.score = 0
        self.playing = 1

    def reset(self):
        self.score = 0
        self.playing = 0
        self.user = -1

    def increment_score(self):
        self.score += 1
        self.socket.emit('currentGame' , self.tojson()  , room = 'play' )
        print('GAME: new score ' + str(self.score))

    def  tojson(self):
        json = {}
        json["score"] = self.score
        json["playing"] =  self.playing
        json["user"] = self.user
        return json
