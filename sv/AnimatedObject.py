import numpy as np
from sv.conn import Conn

class AnimatedObject():
    maxframe = 0
    id = 0
    primitive_obj_ids = ["cube","uv_sphere","torus","monkey","circle","plane","cone","cylinder","grid","ico_sphere","cube_mesh"]

    def __init__(self,connection:Conn,position_data:list[float],object_mesh:str=None,name:str=None,**kwargs) -> None:

        self.positions = position_data
        # self.object_fp = object
        self.conn = connection

        self.id = AnimatedObject.id
        AnimatedObject.id+=1

        if not name:
            self.name =self.id
        else:
            self.name = name


        if object_mesh in self.primitive_obj_ids:
            # Conn.bpy.ops.mesh.primitive_cube_add(3)
            state = self.conn.get_primitive(object_mesh,**kwargs)
            
            # object will be selected when created
            self.instance = self.conn.bpy.context.selected_objects[0]
            self.instance.name = self.name
            self.instance.select_set(False)
        
        for i,frame_pos in enumerate(position_data):
            self.instance.location = frame_pos
            self.instance.keyframe_insert("location",frame=i)

    def delete_object(self):

        self.instance.select_set(True)
        self.conn.bpy.ops.object.delete(True)



        