from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import random

base = ShowBase()

gridSize = 16 # Both dimensions of the grid. The grid will wrap.
interval = 2

grid = [] # This will be filled of arrays full of True (living cells) and False (dead cells)

# Camera setup
base.disableMouse()
base.camera.setPos(gridSize/2, gridSize/2, gridSize*2.5)
base.camera.setP(270)

class Cell:
    def __init__(self, alive):
        self.model = loader.loadModel('gfx/block')
        self.model.reparentTo(render)
        self.alive = alive

    def draw(self):
        if self.alive:
            self.model.show()
        else:
            self.model.hide()

def initialize():
    # Create a 2D array, so that a cell may be looked at by using [x][y]. Also create initial grid
    for x in xrange(0, gridSize):
        row = []
        for y in xrange (0, gridSize):
            row.append(Cell(random.choice([True, False])))
        grid.append(row)
        draw()

def draw():
    for row in grid:
        for cell in row:
            cell.model.setPos(grid.index(row), row.index(cell), 0)
            cell.draw()

initialize()
base.run()