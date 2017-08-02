from random import choice


class Coord:
    def __init__(self, x, y):
        self.worldcoords = [x, y]
        self.map_text = choice(["-", "=", "_"])

        self.canstand = True
