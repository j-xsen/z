from tkinter import *
import math
import sched, time
import zombies
from random import randint

class Game(Frame):
	
	def __init__(self,parent):
		Frame.__init__(self,parent,background="black")
		self.parent = parent
		
		self.parent.title("z")
		self.pack(fill=BOTH,expand=1)
		
		self.center()
		
	def center(self):
		w = 900
		h = 550
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		
		x = (sw - w) / 2
		y = (sh - h) / 2
		self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))
		
		# create canvas
		canvas = Canvas(self,bg='black')
		self.canvas = canvas
		canvas.pack(fill=BOTH,expand=1)
		
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
				c = Cell(col,row * 50,canvas,self.parent,1,[colcoord,row],self.parent,self.map)
			else:
				c = Cell(col,row * 50,canvas,self.parent,0,[colcoord,row],self.parent,self.map)
				
			self.cells.append(c)
			
		# inputs
		self.parent.bind("<Key>",self.kpress)
		self.parent.bind("<KeyRelease>",self.kup)
		self.lmove = False
		self.rmove = False
		self.umove = False
		self.dmove = False
		
		# things to appear in the side menu
		self.updateCoords()
		
	def kpress(self,event):
		if event.char == 's':
			self.saveGame(True)
		elif event.keysym == 'Left':
			self.moveLeft()
		elif event.keysym == 'Right':
			self.moveRight()
		elif event.keysym == 'Up':
			self.moveUp()
		elif event.keysym == 'Down':
			self.moveDown()
			
	def kup(self,event):
		if event.keysym == 'Left':
			self.lmove = False
		elif event.keysym == 'Right':
			self.rmove = False
		elif event.keysym == 'Up':
			self.umove = False
		elif event.keysym == 'Down':
			self.dmove = False
			
	def moveLeft(self):
		# make sure block to the left is viable
		if self.cells[59].canstand == True and self.lmove == False:
			for x in range(0,len(self.cells)):
				thisC = self.cells[x]
				thisC.worldcoords = [thisC.worldcoords[0] - 1, thisC.worldcoords[1]]
				thisC.norepCheckCellZombie()
			
			self.lmove = True
			self.updateCoords()
	def moveRight(self):
		# make sure the block to the right is viable
		if self.cells[61].canstand == True and self.rmove == False:
			for x in range(0,len(self.cells)):
				thisC = self.cells[x]
				thisC.worldcoords = [thisC.worldcoords[0] + 1, thisC.worldcoords[1]]
				thisC.norepCheckCellZombie()
			
			self.rmove = True
			self.updateCoords()
	def moveUp(self):
		# make sure the block above is viable
		if self.cells[49].canstand == True and self.umove == False:
			for x in range(0,len(self.cells)):
				thisC = self.cells[x]
				thisC.worldcoords = [thisC.worldcoords[0], thisC.worldcoords[1] - 1]
				thisC.norepCheckCellZombie()
			
			self.umove = True
			self.updateCoords()
	def moveDown(self):
		# make sure the block above is viable
		if self.cells[71].canstand == True and self.dmove == False:
			for x in range(0,len(self.cells)):
				thisC = self.cells[x]
				thisC.worldcoords = [thisC.worldcoords[0], thisC.worldcoords[1] + 1]
				thisC.norepCheckCellZombie()
			
			self.dmove = True
			self.updateCoords()
			
	def zombCheck(self):
		# check zombie moves
		for x in range(0,len(self.cells)):
			thisC = self.cells[x]
			thisC.norepCheckCellZombie()
			
	def saveGame(self, which):
		if which == True:
			f = open('m.txt','w+')
			f.write("%a" % (self.map))
			f.close()
			self.cells[60].canvas.itemconfig(self.cells[60].missed,text="saved!")
			self.parent.after(1000,self.saveGame,False)
		else:
			self.cells[60].canvas.itemconfig(self.cells[60].missed,text="")
			
	def updateCoords(self):
		setcoords = "coords: %a" % (self.cells[60].worldcoords)
		self.canvas.itemconfig(self.coords,text="%s" % (setcoords))
		
class Cell():
	def __init__(self, x, y, canvas, parent, isplayer, worldcoords, root, map):
		self.canvas = canvas
		self.parent = parent
		self.x = x
		self.y = y
		self.root = root
		self.worldcoords = worldcoords
		self.map = map
		
		self.canstand = True
		
		self.zs = []
		
		# gun time
		self.guntime = 0
		self.gClick = False
		
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
		
		# this shouldn't be needed know zombies auto update via zombies.py
		# self.checkCellZombie()
		
	def norepCheckCellZombie(self):
		# get zombies
		allzs = zombies.getAll()
		
		self.clearCellZombie()
		
		for x in range(0,len(allzs)):
			thiscoords = allzs[x].worldcoords
			if self.worldcoords == thiscoords:
				self.addCellZombie(10)
				self.l.config(fg="red")
				
		# show grass if no zombies AND ISNT PLAYER
		if len(self.zs) == 0 and self.isplayer == 0:
			# check if in bounds
			if self.worldcoords[0] < len(self.map[0]) and self.worldcoords[1] < len(self.map) and self.worldcoords[0] >= 0 and self.worldcoords[1] >= 0:
				idone = self.worldcoords[0]
				idtwo = self.worldcoords[1]
				
				self.updateTxt(self.map[idone][idtwo])
				self.canstand = True
			else:
				self.updateTxt("")
				self.canstand = False
	
	def checkCellZombie(self):
		self.norepCheckCellZombie()
		
		self.root.after(1000,self.checkCellZombie)
		
	def addCellZombie(self,health):
		self.zs.append(health)
		self.updateTxt("O")
		
	def clearCellZombie(self):
		self.zs = []
		if self.isplayer == True:
			self.updateTxt("x")
			self.l.config(fg="green")
		else:
			self.updateTxt("o")
			self.l.config(fg="white")
	
	def clickDown(self,event):
		self.gClick = True
		self.startGun()
	
	def clickUp(self,event):
		self.gClick = False
		
	def startGun(self):
		self.guntime = 0
		self.addGun(self.worldcoords)
		
	def addGun(self,wc):
		if self.gClick == True and self.isplayer == False:
			# check if it's time to shoot
			if self.guntime == 3:
				self.shootGun()
			else:
				if self.worldcoords == wc:
					self.guntime = self.guntime + 1
		
					settxt = ""
		
					for x in range(0,self.guntime):
						settxt = "%s." % (settxt)
			
					self.canvas.itemconfig(self.gun,text=settxt)
			
					self.root.after(500,self.addGun,self.worldcoords)
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
		if len(self.zs) > 90:
			roll = randint(1,100)
			if roll <= 0:
				self.zs = []
				zombies.killZombie(self.worldcoords)
				self.clearCellZombie()
				print("killed zombie @%a!" % (self.worldcoords))
			else:
				self.didMiss(True)
				self.l.config(fg="black")
			
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
		if which == True:
			self.canvas.itemconfig(self.missed,text="missed!")
			self.root.after(500,self.didMiss,False)
		else:
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
		
		zombies.start(self.app)
		self.root.protocol("WM_DELETE_WINDOW",self.closing)
	
		self.root.mainloop()
		
	def closing(self):
		print("closing!")
		zombies.stop()
		self.root.destroy()

def main():
	g = m()
	
if __name__ == '__main__':
	main()
