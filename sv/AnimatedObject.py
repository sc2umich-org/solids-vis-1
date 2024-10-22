import numpy as np
from sv.Conn import Conn

class AnimatedObject():
    maxframe = 0
    def __init__(self,connection:Conn,position_data:list[float],object_name:str=None) -> None:
        self.positions = position_data
        self.object_fp = object
        self.conn = connection

        primitive_objs = {
            "cube":connection.bpy.ops.mesh.primitive_cube_add,
            "uv_sphere":connection.bpy.ops.primitive_uv_sphere_add
        }

        if object in list(self.primitive_objs.keys()):
            # Conn.bpy.ops.mesh.primitive_cube_add(3)
            state = primitive_objs[object_name]()
            try:
                self.sphere = Conn.bpy.data.objects['Sphere']
                self.sphere.select_set(False)
                print("sphere")
            except:
                print("didnt work")

        


        