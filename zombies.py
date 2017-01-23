import threading
import time
from random import randint
import game

class Zombies():
	def __init__(self,x,y):
		self.x = x
		self.y = y
		
		self.num = x * y
		self.worldcoords = [x,y]
		
		print("created zombie @%d,%d(%d)" % (x, y,self.num))


zombs = []
def getAll():
	return zombs
	
def killZombie(worldcoords):
	sel = -1
	for x in range(0,len(zombs)):
		thiszomb = zombs[x]
		if thiszomb.worldcoords == worldcoords:
			sel = x
			print("%d // %a | %a" % (x,thiszomb.worldcoords,worldcoords))
			
	if sel != -1:
		print("%d" % (sel))
		del zombs[sel]
		game.zombCheck()
	
def start(g):
	print("starting...")
	
	global game
	game = g
	
	# create zombies
	createZombie(10)
	
	# start thread to move zombies
	th.start()
	
def createZombie(howmany):
	print("creating zombie...")
	
	# create them
	for x in range(0,howmany):
		z = Zombies(randint(1,21),randint(1,21))
		zombs.append(z)

def stop():
	th.do_run = False
	th.join()

def moveZombies():
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		print("running...")
		
		# for each zombie
		for x in range(0,len(zombs)):
			movex = randint(-1,1)
			movey = randint(-1,1)
			
			thisZ = zombs[x]
			
			# make sure they don't go out of range
			if thisZ.worldcoords[0] + movex > 21 or thisZ.worldcoords[0] + movex < 0:
				print("zombie tried going to location %a, but it's out of range!" % (thisZ.worldcoords[0] + movex))
				movex = 0
			if thisZ.worldcoords[1] + movey > 21 or thisZ.worldcoords[1] + movey < 0:
				print("zombie tried going to location %a, but it's out of range!" % (thisZ.worldcoords[1] + movey))
				movey = 0
				
			thisZ.worldcoords = [thisZ.worldcoords[0] + movex, thisZ.worldcoords[1] + movey]
			print(thisZ.worldcoords)
		
		game.zombCheck()
		time.sleep(5)
	print("stopping...")
	
th = threading.Thread(target=moveZombies)
