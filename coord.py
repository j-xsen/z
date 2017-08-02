from random import choice


class Coord:
    def __init__(self, x, y, game):
        self.worldcoords = [x, y]
        self.map_text = choice(["-", "=", "_"])
        self.g = game

    def canstand(self):
        # return true if no zombies standing here
        return not self.g.get_zombie(self.worldcoords)
