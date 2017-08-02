class Player:
    def __init__(self, game):
        self.g = game
        self.canmove = True

        # move delay
        self.movedelay = 500

        # location
        self.worldcoords = [0, 0]

        # progression
        self.xp = 0
        self.level = 1

    # XP FUNCTIONS #
    def add_xp(self, amount):
        self.xp += amount
        self.g.update_xp()
        if self.xp >= self.get_xp_for_next_level():
            self.level_up()

    def level_up(self):
        self.xp -= self.get_xp_for_next_level()
        self.level += 1
        self.g.update_xp()

    def get_xp_for_next_level(self):
        return self.level ** 2 + 15 * self.level

    # MOVE FUNCTIONS #
    def move_left(self):
        # make sure block to the left is viable
        new_coords = [self.worldcoords[0] - 1, self.worldcoords[1]]
        if self.g.get_coord(new_coords):
            if self.g.get_coord(new_coords).canstand and self.canmove:
                self.worldcoords = new_coords
                self.recenter_cells()
                self.canmove = False
                self.g.update_coords()
                self.g.parent.after(self.movedelay, self.allow_move)

    def move_right(self):
        # make sure the block to the right is viable
        new_coords = [self.worldcoords[0] + 1, self.worldcoords[1]]
        if self.g.get_coord(new_coords):
            if self.g.get_coord(new_coords).canstand and self.canmove:
                self.worldcoords = new_coords
                self.recenter_cells()
                self.canmove = False
                self.g.update_coords()
                self.g.parent.after(self.movedelay, self.allow_move)

    def move_up(self):
        # make sure the block above is viable
        new_coords = [self.worldcoords[0], self.worldcoords[1] - 1]
        if self.g.get_coord(new_coords):
            if self.g.get_coord(new_coords).canstand and self.canmove:
                self.worldcoords = new_coords
                self.recenter_cells()
                self.canmove = False
                self.g.update_coords()
                self.g.parent.after(self.movedelay, self.allow_move)

    def move_down(self):
        # make sure the block below is viable
        new_coords = [self.worldcoords[0], self.worldcoords[1] + 1]
        if self.g.get_coord(new_coords):
            if self.g.get_coord(new_coords).canstand and self.canmove:
                self.worldcoords = new_coords
                self.recenter_cells()
                self.canmove = False
                self.g.update_coords()
                self.g.parent.after(self.movedelay, self.allow_move)

    def recenter_cells(self):
        self.g.recenter_cells()

    def allow_move(self):
        self.canmove = True
