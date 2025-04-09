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

# needs to be a graph, not a tree
# -1 indicates the root
t = [
    {
        "id":0,
        "connections":[{"inp":"Surface","out":"BSDF","id":-1}],
        "node_type":"ShaderNodeBsdfPrincipled",
        "args":{},
    },
    {
        "id":1,
        "node_type": "ShaderNodeMix",
        "connections":[{"inp":"Base Color","out":"Result","id":0}],
        "args":{"data_type":"RGBA"},
    },
    {
        "id":2,
        "node_type": "ShaderNodeBump",
        "connections":[{"inp":"Normal","out":"Normal","id":0}],
        "args":{},
    },
    {
        "id":3,
        "node_type": "ShaderNodeHueSaturation",
        "connections":[{"inp":"Roughness","out":"Color","id":0}],
        "args":{},
    },
    {
        "id":4,
        "node_type": "ShaderNodeDisplacement",
        "connections":[{"inp":"Displacement","out":"Displacement","id":-1}],
        "args":{},
    },
    {
        "id":5,
        "node_type": "ShaderNodeBump",
        "connections":[{"inp":"Normal","out":"Normal","id":2}],
        "args":{},
    },
    {
        "id":6,
        "node_type": "ShaderNodeBump",
        "connections":[{"inp":"Normal","out":"Normal","id":5}],
        "args":{},
    },
    {
        "id":7,
        "node_type": "ShaderNodeMapRange",
        "connections":[
            {"inp":"Factor","out":"Result","id":1},
            {"inp":"Height","out":"Result","id":2}
            ],
        "args":{},
    },
    {
        "id":8,
        "node_type": "ShaderNodeValToRGB",
        "connections":[{"inp":"Color","out":"Color","id":3}],
        "args":{},
    }
]

new_text = Texture(
    "new",
    t
)

planet.instance.data.materials.append(new_text.mat)
bpy_conn.save_blend("tests/blend/texture_test.blend")