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
