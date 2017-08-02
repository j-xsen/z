import math
from random import randint
from tkinter import *

import player
import zombie


class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")
        self.parent = parent

        self.parent.title("z")
        self.pack(fill=BOTH, expand=1)

        self.p = player.Player(self)

        w = 900
        h = 550
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # create canvas
        canvas = Canvas(self, bg='black')
        canvas.pack(fill=BOTH, expand=1)
        self.canvas = canvas

        # create cells
        self.cells = []
        self.map = []

        # create map
        for x in range(0, 22):
            appen = []
            for y in range(0, 22):
                z = randint(1, 3)
                addtxt = "-"
                if z == 1:
                    addtxt = "="
                elif z == 2:
                    addtxt = "_"
                appen.append(addtxt)
            self.map.append(appen)

        self.coords = canvas.create_text(725, 20, text="coords:", fill="white")

        # create cells
        for x in range(0, 121):
            row = (math.floor(x / 11))
            col = (x * 50) - (row * 550)
            colcoord = x - (row * 11)
            # print("%d//%d" % (col,row))

            # set player
            if x == 60:
                c = Cell(col, row * 50, 1, [colcoord, row], self)
            else:
                c = Cell(col, row * 50, 0, [colcoord, row], self)

            self.cells.append(c)

        # inputs
        self.parent.bind("<Key>", self.kpress)
        # self.parent.bind("<KeyRelease>",self.kup)

        # create zombies
        self.zombies = []
        for x in range(0, 10):
            z = zombie.Zombie(self, randint(1, 21), randint(1, 21))
            self.zombies.append(z)

        # version
        self.version = canvas.create_text(725, 525, text="demo 2", fill="white")

        # things to appear in the side menu
        self.update_coords()
        self.xp_holder = canvas.create_rectangle(600, 50, 850, 75, outline="white", fill="black")
        self.xp_bar = canvas.create_rectangle(602, 52, 603, 73, fill="green")
        self.xp_label = canvas.create_text(725, 62.5, text="", fill="white")
        self.xp_level_label = canvas.create_text(725, 85, text=str(self.p.level), fill="white")
        self.update_xp()

    def kpress(self, event):
        if event.keysym == 'Left':
            self.p.move_left()
        elif event.keysym == 'Right':
            self.p.move_right()
        elif event.keysym == 'Up':
            self.p.move_up()
        elif event.keysym == 'Down':
            self.p.move_down()

    def zomb_check(self):
        # check zombie moves
        for x in range(0, len(self.cells)):
            this = self.cells[x]
            this.norep_check_cell_zombie()

    def update_coords(self):
        setcoords = "coords: %a" % self.cells[60].worldcoords
        self.canvas.itemconfig(self.coords, text="%s" % setcoords)

    def update_xp(self):
        maxlength = 848 - 602
        perctonextlvl = self.p.xp / self.p.get_xp_for_next_level()
        self.canvas.coords(self.xp_bar, 602, 52, (maxlength * perctonextlvl) + 602, 73)
        self.canvas.itemconfig(self.xp_label, text=str(self.p.xp) + " / " + str(self.p.get_xp_for_next_level()))
        self.canvas.itemconfig(self.xp_level_label, text="level: " + str(self.p.level))

    # gets cell w/ requested worldcoords
    def get_cell(self, worldcoords):
        for cell in self.cells:
            if cell.worldcoords == worldcoords:
                return cell
        return False

    # get zombie w/ requested worldcoords
    def get_zombie(self, worldcoords):
        for z in self.zombies:
            if z.worldcoords == worldcoords:
                return z
        return False

    # remove zombie w/ requested worldcoords
    def rm_zombie(self, worldcoords):
        self.zombies.remove(self.get_zombie(worldcoords))

    # refreshes all cells
    def refresh_cells(self):
        for cell in self.cells:
            cell.norep_check_cell_zombie()


class Cell:
    def __init__(self, x, y, isplayer, worldcoords, g):
        self.canvas = g.canvas
        self.x = x
        self.y = y
        self.root = g.parent
        self.worldcoords = worldcoords
        self.map = g.map

        self.game = g

        self.canstand = True

        # gun time
        self.guntime = 0
        self.gClick = False

        canvas = self.canvas

        self.r = canvas.create_rectangle(x, y, x + 50, y + 50, outline="white", fill="black", width=1, tags="t")

        # create the visible stuff
        self.l = Label(canvas, text="-", bg="black", fg="white", width=5)
        self.l.place(x=x + 5, y=y + 15)
        self.gun = canvas.create_text(x + 25, y + 40, text="", fill="white")
        self.missed = canvas.create_text(x + 25, y + 10, text="", fill="white")

        # check whether to set this as a player cell or not
        if isplayer == 1:
            self.l.config(text="x")
            self.isplayer = True
        else:
            self.isplayer = False

        # create binds
        canvas.tag_bind(self.r, "<ButtonPress-1>", self.click_down)
        canvas.tag_bind(self.r, "<ButtonRelease-1>", self.click_up)
        self.l.bind("<ButtonPress-1>", self.click_down)
        self.l.bind("<ButtonRelease-1>", self.click_up)

        canvas.pack()

    def norep_check_cell_zombie(self):
        # colors
        if self.isplayer:
            self.update_txt("x")
            self.l.config(fg="green")
        else:
            self.l.config(fg="white")

        if self.game.get_zombie(self.worldcoords):
            zombie = self.game.get_zombie(self.worldcoords)
            if zombie.dead:
                if zombie.deadtick == 0:
                    self.update_txt("o")
                    self.l.config(fg="white")
                    zombie.deadtick = 1
                else:
                    self.game.rm_zombie(self.worldcoords)
            else:
                self.update_txt("O")
                self.l.config(fg="red")

        # show grass if no zombies and isn't player
        if not self.game.get_zombie(self.worldcoords) and not self.isplayer:
            # check if in bounds
            if len(self.map[0]) > self.worldcoords[0] >= 0 and len(self.map) > self.worldcoords[1] >= 0:
                idone = self.worldcoords[0]
                idtwo = self.worldcoords[1]

                self.update_txt(self.map[idone][idtwo])
                self.canstand = True
            else:
                self.update_txt("")
                self.canstand = False

    def click_down(self, event):
        self.gClick = True
        self.start_gun()

    def click_up(self, event):
        self.gClick = False

    def start_gun(self):
        self.guntime = 0
        self.add_gun(self.worldcoords)

    def add_gun(self, wc):
        if self.gClick and not self.isplayer:
            # check if it's time to shoot
            if self.guntime == 3 and self.worldcoords == wc:
                self.shoot_gun()
            else:
                if self.worldcoords == wc:
                    self.guntime = self.guntime + 1

                    settxt = ""
                    for x in range(0, self.guntime):
                        settxt += "."
                    self.canvas.itemconfig(self.gun, text=settxt)

                    self.root.after(500, self.add_gun, wc)
                else:
                    print("moved!")
                    self.remove_gun()
        else:
            self.remove_gun()

    def remove_gun(self):
        self.guntime = 0
        self.canvas.itemconfig(self.gun, text="")

    def shoot_gun(self):
        # check if there are any zombies and if there are, roll to see if it kills
        if self.game.get_zombie(self.worldcoords):
            roll = randint(1, 100)
            if roll >= 10:
                self.game.get_zombie(self.worldcoords).damage(10)
                self.did_miss(False)
            else:
                self.did_miss(True)
                self.l.config(fg="black")

        self.norep_check_cell_zombie()
        self.canvas.itemconfig(self.r, fill="red")
        self.l.config(background="red")
        self.remove_gun()
        self.root.after(500, self.remove_gun_red)

    def remove_gun_red(self):
        self.canvas.itemconfig(self.r, fill="black")
        self.l.config(background="black")
        self.l.config(fg="red")
        self.norep_check_cell_zombie()

    def did_miss(self, which):
        if which:
            self.canvas.itemconfig(self.missed, text="missed!")
        else:
            if self.game.get_zombie(self.worldcoords).dead:
                self.canvas.itemconfig(self.missed, text="killed!")
            else:
                self.canvas.itemconfig(self.missed, text="hit!")
        self.root.after(500, self.fix_miss)

    def fix_miss(self):
        self.canvas.itemconfig(self.missed, text="")

    def update_txt(self, text):
        self.l.config(text=text)
        self.canvas.pack()


class M:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("0x0+0+0")
        self.app = Game(self.root)

        # zombies.start(self.app)
        self.root.protocol("WM_DELETE_WINDOW", self.closing)

        self.root.mainloop()

    def closing(self):
        print("closing!")
        # zombies.stop()
        self.root.destroy()


def main():
    g = M()


if __name__ == '__main__':
    main()
