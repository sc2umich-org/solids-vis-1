import numpy
from sv.conn import Conn

class AnimatedObject():
    maxframe = 0
    primitive_objs = {
        "cube":Conn.bpy.ops.mesh.primitive_cube_add,
        "uv_sphere":Conn.bpy.ops.primitive_uv_sphere_add
    }
    def __init__(self,position_data,object:str) -> None:
        self.positions = position_data
        self.object_fp = object

        if object in list(self.primitive_objs.keys()):
            # Conn.bpy.ops.mesh.primitive_cube_add(3)
            Conn.bpy.ops.mesh.primitive_uv_sphere_add(3)
        


        