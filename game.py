from tkinter import *
import math
import sched, time
import zombies
import gun
import player
from random import randint

class Game(Frame):

	def __init__(self,parent):
		Frame.__init__(self,parent,background="black")
		self.parent = parent

		self.parent.title("z")
		self.pack(fill=BOTH,expand=1)

		self.p = player.Player(self)

		w = 900
		h = 550
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w) / 2
		y = (sh - h) / 2
		self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))

		# create canvas
		canvas = Canvas(self,bg='black')
		canvas.pack(fill=BOTH,expand=1)
		self.canvas = canvas

		# create cells
		self.cells = []
		self.map = []

		# create map
		for x in range(0,22):
			appen = []
			for y in range(0,22):
				z = randint(1,3)
				addtxt = "-"
				if z == 1:
					addtxt = "="
				elif z == 2:
					addtxt = "_"
				appen.append(addtxt)
			self.map.append(appen)

		self.coords = canvas.create_text(725,20,text="coords:",fill="white")

		# create cells
		for x in range(0,121):
			row = (math.floor(x / 11))
			col = (x * 50) - (row * 550)
			colcoord = x - (row * 11)
			# print("%d//%d" % (col,row))

			# set player
			if x == 60:
				c = Cell(col,row * 50,1,[colcoord,row],self)
			else:
				c = Cell(col,row * 50,0,[colcoord,row],self)

			self.cells.append(c)

		# inputs
		self.parent.bind("<Key>",self.kpress)
		#self.parent.bind("<KeyRelease>",self.kup)

		# create zombies
		self.zombies = []
		for x in range(0,10):
			z = zombies.Zombie(self,randint(1,21),randint(1,21))
			self.zombies.append(z)

		# version
		self.version = canvas.create_text(725,525,text="demo 2",fill="white")

		# things to appear in the side menu
		self.updateCoords()

	def kpress(self,event):
		if event.keysym == 'Left':
			self.p.moveLeft()
		elif event.keysym == 'Right':
			self.p.moveRight()
		elif event.keysym == 'Up':
			self.p.moveUp()
		elif event.keysym == 'Down':
			self.p.moveDown()

	# def kup(self,event):
	# 	if event.keysym == 'Left':
	# 		self.lmove = False
	# 	elif event.keysym == 'Right':
	# 		self.rmove = False
	# 	elif event.keysym == 'Up':
	# 		self.umove = False
	# 	elif event.keysym == 'Down':
	# 		self.dmove = False

	def zombCheck(self):
		# check zombie moves
		for x in range(0,len(self.cells)):
			thisC = self.cells[x]
			thisC.norepCheckCellZombie()

	def updateCoords(self):
		setcoords = "coords: %a" % (self.cells[60].worldcoords)
		self.canvas.itemconfig(self.coords,text="%s" % (setcoords))

	# gets cell w/ requested worldcoords
	def getCell(self,worldcoords):
		for cell in self.cells:
			if cell.worldcoords == worldcoords:
				return cell
		return False

	# get zombie w/ requested worldcoords
	def getZombie(self,worldcoords):
		for z in self.zombies:
			if z.worldcoords == worldcoords:
				return z
		return False

	# remove zombie w/ requested worldcoords
	def rmZombie(self,worldcoords):
		self.zombies.remove(self.getZombie(worldcoords))

	# refreshes all cells
	def refreshCells(self):
		for cell in self.cells:
			cell.norepCheckCellZombie()

class Cell():
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

		self.r = canvas.create_rectangle(x,y,x + 50,y + 50,outline="white",fill="black",width=1,tags="t")

		# create the visible stuff
		self.l = Label(canvas,text="-",bg="black",fg="white",width=5)
		self.l.place(x=x+5,y=y+15)
		self.gun = canvas.create_text(x+25,y+40,text="",fill="white")
		self.missed = canvas.create_text(x+25,y+10,text="",fill="white")

		# check whether to set this as a player cell or not
		if isplayer == 1:
			self.l.config(text="x")
			self.isplayer = True
		else:
			self.isplayer = False

		# create binds
		canvas.tag_bind(self.r,"<ButtonPress-1>",self.clickDown)
		canvas.tag_bind(self.r,"<ButtonRelease-1>",self.clickUp)
		self.l.bind("<ButtonPress-1>",self.clickDown)
		self.l.bind("<ButtonRelease-1>",self.clickUp)

		canvas.pack()

	def norepCheckCellZombie(self):
		# colors
		if self.isplayer:
			self.updateTxt("x")
			self.l.config(fg="green")
		else:
			self.l.config(fg="white")

		if self.game.getZombie(self.worldcoords):
			zombie = self.game.getZombie(self.worldcoords)
			if zombie.dead:
				if zombie.deadtick == 0:
					self.updateTxt("o")
					self.l.config(fg="white")
					zombie.deadtick = 1
				else:
					self.game.rmZombie(self.worldcoords)
			else:
				self.updateTxt("O")
				self.l.config(fg="red")

		# show grass if no zombies and isn't player
		if not self.game.getZombie(self.worldcoords) and not self.isplayer:
			# check if in bounds
			if self.worldcoords[0] < len(self.map[0]) and self.worldcoords[1] < len(self.map) and self.worldcoords[0] >= 0 and self.worldcoords[1] >= 0:
				idone = self.worldcoords[0]
				idtwo = self.worldcoords[1]

				self.updateTxt(self.map[idone][idtwo])
				self.canstand = True
			else:
				self.updateTxt("")
				self.canstand = False

	def clickDown(self,event):
		self.gClick = True
		self.startGun()

	def clickUp(self,event):
		self.gClick = False

	def startGun(self):
		self.guntime = 0
		self.addGun(self.worldcoords)

	def addGun(self,wc):
		if self.gClick and not self.isplayer:
			# check if it's time to shoot
			if self.guntime == 3 and self.worldcoords == wc:
				self.shootGun()
			else:
				if self.worldcoords == wc:
					self.guntime = self.guntime + 1

					settxt = ""
					for x in range(0,self.guntime):
						settxt += "."
					self.canvas.itemconfig(self.gun,text=settxt)

					self.root.after(500,self.addGun,wc)
				else:
					print("moved!")
					self.removeGun()
		else:
			self.removeGun()

	def removeGun(self):
		self.guntime = 0
		self.canvas.itemconfig(self.gun,text="")

	def shootGun(self):
		# check if there are any zombies and if there are, roll to see if it kills
		if self.game.getZombie(self.worldcoords):
			roll = randint(1,100)
			if roll >= 10:
				self.game.getZombie(self.worldcoords).damage(10)
				self.didMiss(False)
			else:
				self.didMiss(True)
				self.l.config(fg="black")

		self.norepCheckCellZombie()
		self.canvas.itemconfig(self.r,fill="red")
		self.l.config(background="red")
		self.removeGun()
		self.root.after(500,self.removeGunRed)

	def removeGunRed(self):
		self.canvas.itemconfig(self.r,fill="black")
		self.l.config(background="black")
		self.l.config(fg="red")
		self.norepCheckCellZombie()

	def didMiss(self,which):
		if which:
			self.canvas.itemconfig(self.missed,text="missed!")
		else:
			if self.game.getZombie(self.worldcoords).dead:
				self.canvas.itemconfig(self.missed,text="killed!")
			else:
				self.canvas.itemconfig(self.missed,text="hit!")
		self.root.after(500,self.fixMiss)

	def fixMiss(self):
		self.canvas.itemconfig(self.missed,text="")

	def updateTxt(self,text):
		self.text = text

		self.l.config(text=self.text)

		self.canvas.pack()

class m():
	def __init__(self):
		self.root = Tk()
		self.root.geometry("0x0+0+0")
		self.app = Game(self.root)

		# zombies.start(self.app)
		self.root.protocol("WM_DELETE_WINDOW",self.closing)

		self.root.mainloop()

	def closing(self):
		print("closing!")
		# zombies.stop()
		self.root.destroy()

def main():
	g = m()

if __name__ == '__main__':
	main()
