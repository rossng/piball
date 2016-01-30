from piball.control.output import PiballOutputHandler


class PiballGame:
    def __init__(self, output_handler: PiballOutputHandler):
        self.output_handler = output_handler
        self.score = 0
        self.reset()

    def reset(self):
        self.score = 0

    def increment_score(self):
        self.score += 1
        print('GAME: new score ' + str(self.score))

