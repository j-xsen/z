class Player():
    def __init__(self, game):
        self.g = game
        self.canmove = True
        print("done:)")

    def move_left(self):
        # make sure block to the left is viable
        if self.g.cells[59].canstand and self.canmove:
            for x in range(0, len(self.g.cells)):
                this = self.g.cells[x]
                this.worldcoords = [this.worldcoords[0] - 1, this.worldcoords[1]]
                this.norep_check_cell_zombie()
            self.canmove = False
            self.g.update_coords()
            self.g.parent.after(1000, self.allow_move)

    def move_right(self):
        # make sure the block to the right is viable
        if self.g.cells[61].canstand and self.canmove:
            for x in range(0, len(self.g.cells)):
                this = self.g.cells[x]
                this.worldcoords = [this.worldcoords[0] + 1, this.worldcoords[1]]
                this.norep_check_cell_zombie()
            self.canmove = False
            self.g.update_coords()
            self.g.parent.after(1000, self.allow_move)

    def move_up(self):
        # make sure the block above is viable
        if self.g.cells[49].canstand and self.canmove:
            for x in range(0, len(self.g.cells)):
                this = self.g.cells[x]
                this.worldcoords = [this.worldcoords[0], this.worldcoords[1] - 1]
                this.norep_check_cell_zombie()
            self.canmove = False
            self.g.update_coords()
            self.g.parent.after(1000, self.allow_move)

    def move_down(self):
        # make sure the block below is viable
        if self.g.cells[71].canstand and self.canmove:
            for x in range(0, len(self.g.cells)):
                this = self.g.cells[x]
                this.worldcoords = [this.worldcoords[0], this.worldcoords[1] + 1]
                this.norep_check_cell_zombie()
            self.canmove = False
            self.g.update_coords()
            self.g.parent.after(1000, self.allow_move)

    def allow_move(self):
        self.canmove = True
