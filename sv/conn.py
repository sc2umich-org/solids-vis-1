import bpy

class Conn():
    # potentially add option to have multiple blenders at once
    # https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html#limitations
    # https://stackoverflow.com/questions/28075599/opening-blend-files-using-blenders-python-api

    def __init__(self) -> None:
        self.bpy=bpy
        self.primitive_objs = {
            "cube":self.bpy.ops.mesh.primitive_cube_add,
            "uv_sphere":self.bpy.ops.mesh.primitive_uv_sphere_add
        }
    def get_primitive(self,obj_type):
        return self.primitive_objs[obj_type]()