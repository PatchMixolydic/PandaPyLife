from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.task import Task
import random

base = ShowBase()

gridSize = 16 # Both dimensions of the grid. The grid will wrap.
interval = 2

loopRunning = False
runButton = None
grid = []

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
    global runButton

    # Camera setup
    base.disableMouse()
    base.camera.setPos(gridSize/2, gridSize/2, gridSize*2.5)
    base.camera.setP(270)

    # DirectGui
    stepButton = DirectButton(text = ("Step", "Step", "Step", "Step"), scale = 0.05, command = step, pos = (-0.25, 0, 0.75))
    runButton = DirectButton(text = ("Run", "Run", "Run", "Run"), scale = 0.05, command = toggleRun, pos = (0.25, 0, 0.75))

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

def getCellAlive(cellX, cellY):
    try:
        grid[cellX][cellY]
    except:
        if cellX >= gridSize:
            cellX = 0
        elif cellX <= 0:
            cellX = gridSize - 1

        if cellY >= gridSize:
            cellY = 0
        elif cellY <= 0:
            cellY = gridSize - 1

    return grid[cellX][cellY].alive

def step():
    """
    Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by over-population.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    -https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """
    for x in grid:
        for y in x:
            neighbors = [getCellAlive(grid.index(x)-1, x.index(y)), getCellAlive(grid.index(x)-1, x.index(y)-1), getCellAlive(grid.index(x)-1, x.index(y)+1), getCellAlive(grid.index(x)+1, x.index(y)),
                         getCellAlive(grid.index(x)+1, x.index(y)-1), getCellAlive(grid.index(x)+1, x.index(y)+1), getCellAlive(grid.index(x), x.index(y)-1), getCellAlive(grid.index(x), x.index(y)+1)]
            if y.alive:
                if neighbors.count(True) < 2 or neighbors.count(True) > 3:
                    y.alive = False
            elif neighbors.count(True) == 3:
                y.alive = True
    draw()

def toggleRun():
    global loopRunning
    if loopRunning:
        loopRunning = False
        runButton["text"] = ("Run", "Run", "Run", "Run")
        taskMgr.remove("Run Loop")
    else:
        loopRunning = True
        runButton["text"] = ("Stop", "Stop", "Stop", "Stop")
        taskMgr.add(runLoop, "Run Loop")

def runLoop(task):
    step()
    return task.cont

initialize()
base.run()