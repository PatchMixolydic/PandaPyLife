from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.task import Task
import random

loadPrcFileData('', 'window-title Conway\'s Game of Life')

base = ShowBase()

gridSize = 16 # Both dimensions of the grid. The grid will wrap.

loopRunning = False
stepButton = None
runButton = None
editButton = None
editMode = False
grid = []
liveGrid = []
newGridTemp = []

class Cell:
    def __init__(self, alive):
        self.model = loader.loadModel('gfx/block')
        self.model.reparentTo(render)
        self.alive = alive
        self.model.setTag('cell', '1')

    def draw(self):
        if self.alive:
            self.model.show()
            self.model.setColorScale(1,1,1,1)
        else:
            if editMode:
                self.model.show()
                self.model.setColorScale(0.5,0.5,0.5,1)
            else:
                self.model.hide()

def initialize():
    global stepButton
    global runButton
    global editButton

    # Camera setup
    base.disableMouse()
    base.camera.setPos(gridSize/2, gridSize/2, gridSize*2.5)
    base.camera.setP(270)

    # DirectGui
    stepButton = DirectButton(text = ("Step", "Step", "Step", "Step"), scale = 0.05, command = step, pos = (-0.33, 0, 0.75))
    runButton = DirectButton(text = ("Run", "Run", "Run", "Run"), scale = 0.05, command = toggleRun, pos = (0, 0, 0.75))
    editButton = DirectButton(text = ("Edit", "Edit", "Edit", "Edit"), scale = 0.05, command = toggleEdit, pos = (0.33, 0, 0.75))

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
        liveGrid[cellX][cellY]
    except:
        if cellX >= gridSize:
            cellX = 0
        elif cellX < 0:
            cellX = gridSize - 1

        if cellY >= gridSize:
            cellY = 0
        elif cellY < 0:
            cellY = gridSize - 1

    return liveGrid[cellX][cellY]

def step():
    """
    Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by over-population.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    -https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """
    global liveGrid
    liveGrid = []

    for x in xrange(0, gridSize):
        liveGrid.append([])

    for x in grid:
        for y in x:
            liveGrid[grid.index(x)].append(y.alive)

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

def toggleEdit():
    global editMode
    if loopRunning:
        toggleRun()
    if editMode:
        editMode = False
        editButton["text"] = ("Edit", "Edit", "Edit", "Edit")
        stepButton["text"] = ("Step", "Step", "Step", "Step")
        stepButton["command"] = step
        runButton.show()
    else:
        editMode = True
        editButton["text"] = ("Back", "Back", "Back", "Back")
        stepButton["text"] = ("Clear", "Clear", "Clear", "Clear")
        stepButton["command"] = clearGrid
        runButton.hide()
    draw()

traverser = CollisionTraverser()
handler = CollisionHandlerQueue()

pickerNode = CollisionNode('mouseRay')
pickerNP = camera.attachNewNode(pickerNode)
pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
pickerRay = CollisionRay()
pickerNode.addSolid(pickerRay)
traverser.addCollider(pickerNP, handler)

def handlePick():
    if not editMode:
        return

    if base.mouseWatcherNode.hasMouse():
        mpos = base.mouseWatcherNode.getMouse()
        pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

        traverser.traverse(render)
        if handler.getNumEntries() > 0:
            handler.sortEntries()
            pickedObj = handler.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('cell')
            if not pickedObj.isEmpty():
                cell = grid[int(pickedObj.getX())][int(pickedObj.getY())]
                cell.alive = not cell.alive
                cell.draw()

def clearGrid():
    for row in grid:
        for cell in row:
            cell.alive = False
    draw()

base.accept('mouse1', handlePick)

initialize()
base.run()