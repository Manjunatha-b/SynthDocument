from Src.Canvas import Canvas


class Synthesizer():
    def __init__(self):
        self.canvas = Canvas()
        self.canvas.save('result.png')


Synthesizer()
