# import threading
# import time
from random import randint, choice
import random
import game

class Zombie():
	def __init__(self,game,x,y):
		self.game = game

		self.x = x
		self.y = y
		self.worldcoords = [x,y]

		self.ticksincelastmove = 0

		self.health = randint(10,20)
		self.dead = False
		self.deadtick = 0

		self.move()

		print("created zombie @%d,%d(%d)" % (self.x, self.y, self.health))

	def move(self):
		# choose a direction
		direction = choice(["n"])

		if direction == "n":
			goalcell = self.game.getCell([self.worldcoords[0],self.worldcoords[1] - 1])
			if goalcell:
				if goalcell.canstand:
					self.worldcoords = goalcell.worldcoords
				# else:
					# print("zombie tried leaving area")

		self.game.refreshCells()
		self.game.parent.after(5000,self.move)

	def damage(self, dmg):
		self.health -= dmg
		if self.health <= 0:
			print("killed me!")
			self.dead = True

# def start(g):
# 	print("starting...")

	# global game
	# game = g

	# create zombies
	# createZombie(10)

	# start thread to move zombies
	# th.start()

# def createZombie(howmany):
# 	print("creating zombie...")
#
# 	# create them
# 	for x in range(0,howmany):
# 		z = Zombies(randint(1,21),randint(1,21))
# 		zombs.append(z)

# def stop():
# 	th.do_run = False
# 	th.join()

# def moveZombies():
# 	t = threading.currentThread()
# 	while getattr(t, "do_run", True):
# 		print("running...")
#
# 		# for each zombie
# 		for x in range(0,len(zombs)):
# 			movex = randint(-1,1)
# 			movey = randint(-1,1)
#
# 			thisZ = zombs[x]
#
# 			# make sure they don't go out of range
# 			if thisZ.worldcoords[0] + movex > 21 or thisZ.worldcoords[0] + movex < 0:
# 				print("zombie tried going to location %a, but it's out of range!" % (thisZ.worldcoords[0] + movex))
# 				movex = 0
# 			if thisZ.worldcoords[1] + movey > 21 or thisZ.worldcoords[1] + movey < 0:
# 				print("zombie tried going to location %a, but it's out of range!" % (thisZ.worldcoords[1] + movey))
# 				movey = 0
#
# 			thisZ.worldcoords = [thisZ.worldcoords[0] + movex, thisZ.worldcoords[1] + movey]
# 			print(thisZ.worldcoords)
#
# 		game.zombCheck()
# 		time.sleep(5)
# 	print("stopping...")
#
# th = threading.Thread(target=moveZombies)
