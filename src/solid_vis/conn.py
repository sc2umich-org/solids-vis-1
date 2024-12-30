import bpy
import mathutils

class Conn():
    # potentially add option to have multiple blenders at once
    # https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html#limitations
    # https://stackoverflow.com/questions/28075599/opening-blend-files-using-blenders-python-api

    def __init__(self) -> None:
        self.bpy=bpy
        self.mathutils = mathutils
        self.primitive_objs = {
            "cube":self.bpy.ops.mesh.primitive_cube_add,
            "uv_sphere":self.bpy.ops.mesh.primitive_uv_sphere_add,
            "torus":self.bpy.ops.mesh.primitive_torus_add,
            "monkey":self.bpy.ops.mesh.primitive_monkey_add,
            "circle":self.bpy.ops.mesh.primitive_circle_add,
            "plane":self.bpy.ops.mesh.primitive_plane_add,
            "cone":self.bpy.ops.mesh.primitive_cone_add,
            "cylinder":self.bpy.ops.mesh.primitive_cylinder_add,
            "grid":self.bpy.ops.mesh.primitive_grid_add,
            "ico_sphere":self.bpy.ops.mesh.primitive_ico_sphere_add
        }
    def get_primitive(self,obj_type,**kwargs):
        return self.primitive_objs[obj_type](**kwargs)