from random import randint, choice


class Zombie:
    def __init__(self, game, x, y):
        self.game = game

        self.x = x
        self.y = y
        self.worldcoords = [x, y]

        self.ticksincelastmove = 0

        self.health = randint(10, 20)
        self.starthealth = self.health
        self.dead = False
        self.deadtick = 0

        self.move()

        print("created zombie @%d,%d(%d)" % (self.x, self.y, self.health))

    def move(self):
        # choose a direction
        direction = choice(["n", "ne", "e", "es", "s", "sw", "w", "nw"])

        # percentage moving
        if randint(1, 100) < 75:
            if "n" in direction:
                self.north()
            elif "s" in direction:
                self.south()
            elif "e" in direction:
                self.east()
            elif "w" in direction:
                self.west()

        self.game.refresh_cells()
        self.game.parent.after(5000, self.move)

    def north(self):
        goalcell = self.game.get_cell([self.worldcoords[0], self.worldcoords[1] - 1])
        if goalcell:
            if goalcell.canstand:
                self.worldcoords = goalcell.worldcoords

    def south(self):
        goalcell = self.game.get_cell([self.worldcoords[0], self.worldcoords[1] + 1])
        if goalcell:
            if goalcell.canstand:
                self.worldcoords = goalcell.worldcoords

    def east(self):
        goalcell = self.game.get_cell([self.worldcoords[0] + 1, self.worldcoords[1]])
        if goalcell:
            if goalcell.canstand:
                self.worldcoords = goalcell.worldcoords

    def west(self):
        goalcell = self.game.get_cell([self.worldcoords[0] - 1, self.worldcoords[1]])
        if goalcell:
            if goalcell.canstand:
                self.worldcoords = goalcell.worldcoords

    def damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.dead = True
            self.game.p.add_xp(self.starthealth)
