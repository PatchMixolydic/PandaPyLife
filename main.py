from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import random

base = ShowBase()

base.disableMouse()

base.camera.setZ(25)
base.camera.setP(270)

test = loader.loadModel('gfx/block')
test.reparentTo(render)

base.run()