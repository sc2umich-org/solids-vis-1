from solid_vis import conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
from solid_vis.texture import tex_from_blend
import numpy as np
import bpy

t = tex_from_blend("examples/blend/slingshot.blend","moon surface")
print(t)