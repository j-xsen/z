from random import choice, randint


class Coord:
    def __init__(self, x, y, game):
        self.worldcoords = [x, y]
        self.map_text = choice(["-", "=", "_"])
        self.g = game

        self.status = "normal"

        # gun vars
        self.guntime = 0
        self.guntext = ""
        self.missedtext = ""
        self.still_gun = False
        self.did_miss = False

    def canstand(self):
        # return true if no zombies standing here
        return not self.g.get_zombie(self.worldcoords)

    # GUN FUNCTIONS #
    def start_gun(self):
        self.guntime = 0
        self.still_gun = True
        self.add_gun()

    def end_gun(self):
        self.guntime = 0
        self.still_gun = False
        self.guntext = ""

    def gun_miss(self, which):
        if which:
            self.missedtext = "missed!"
        else:
            if self.g.get_zombie(self.worldcoords):
                if self.g.get_zombie(self.worldcoords).dead:
                    self.missedtext = "killed!"
                else:
                    self.missedtext = "hit!"
            else:
                self.missedtext = ""

        self.g.get_cell(self.worldcoords).norep_check_cell_zombie()
        self.g.parent.after(500, self.gun_fix_miss)

    def gun_fix_miss(self):
        self.missedtext = ""
        self.g.get_cell(self.worldcoords).norep_check_cell_zombie()

    def add_gun(self):
        if not self.g.is_player_here(self.worldcoords) and self.still_gun:
            # check if it's time to shoot
            if self.guntime == 3:
                self.shoot_gun()
            else:
                self.guntime += 1

                settxt = ""
                for x in range(0, self.guntime):
                    settxt += "."
                self.guntext = settxt

                self.g.parent.after(500, self.add_gun)
        else:
            self.end_gun()

        self.g.get_cell(self.worldcoords).norep_check_cell_zombie()

    def shoot_gun(self):
        # check if there are any zombies and if there are, roll to see if it kills
        if self.g.get_zombie(self.worldcoords):
            if randint(1, 100) >= 10:
                self.g.get_zombie(self.worldcoords).damage(10)
                self.gun_miss(False)
            else:
                self.gun_miss(True)

        self.g.get_cell(self.worldcoords).norep_check_cell_zombie()
        self.end_gun()
