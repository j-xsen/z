
class Player():

    def __init__(self,game):
        # input stuff
        # self.lmove = False
		# self.rmove = False
		# self.umove = False
		# self.dmove = False
        self.g = game
        print("done:)")

    def moveLeft(self):
    	# make sure block to the left is viable
    	if self.g.cells[59].canstand:
    		for x in range(0,len(self.g.cells)):
    			thisC = self.g.cells[x]
    			thisC.worldcoords = [thisC.worldcoords[0] - 1, thisC.worldcoords[1]]
    			thisC.norepCheckCellZombie()

    		# self.lmove = True
    		self.g.updateCoords()

    def moveRight(self):
    	# make sure the block to the right is viable
    	if self.g.cells[61].canstand:
    		for x in range(0,len(self.g.cells)):
    			thisC = self.g.cells[x]
    			thisC.worldcoords = [thisC.worldcoords[0] + 1, thisC.worldcoords[1]]
    			thisC.norepCheckCellZombie()

    		# self.rmove = True
    		self.g.updateCoords()

    def moveUp(self):
    	# make sure the block above is viable
        if self.g.cells[49].canstand:
            for x in range(0,len(self.g.cells)):
                thisC = self.g.cells[x]
                thisC.worldcoords = [thisC.worldcoords[0], thisC.worldcoords[1] - 1]
                thisC.norepCheckCellZombie()

            self.g.updateCoords()

    def moveDown(self):
		# make sure the block above is viable
        if self.g.cells[71].canstand:
            for x in range(0,len(self.g.cells)):
                thisC = self.g.cells[x]
                thisC.worldcoords = [thisC.worldcoords[0], thisC.worldcoords[1] + 1]
                thisC.norepCheckCellZombie()

            # self.dmove = True
            self.g.updateCoords()
