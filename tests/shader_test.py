from solid_vis import conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
from solid_vis.texture import Texture
import numpy as np
import bpy

bpy_conn = conn.Conn()

frames = [0]
scale = 0.1
positions = [[100,-100,30]]

scene = Scene(bpy_conn)
planet = AnimatedObject(
        bpy_conn,
        positions,
        "uv_sphere",
        "planet",
        radius = 3
    )

t = [{
    "output":"BSDF",
    "parent_input":"Surface",
    "node_type":"ShaderNodeBsdfPrincipled",
    "args":{

    },
    "children":[
        {
            "node_type": "ShaderNodeMixRGB", # node.bl_idname
            "args":{},
            "output":"Color",
            "parent_input":"Base Color"
        }
    ]
}]

new_text = Texture(
    "new",
    t
)

planet.instance.data.materials.append(new_text.mat)
bpy_conn.save_blend("tests/blend/texture_test.blend")