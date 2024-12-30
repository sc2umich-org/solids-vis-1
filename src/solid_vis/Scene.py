import solid_vis.conn as conn
from solid_vis.AnimatedObject import AnimatedObject
import os

class Scene():
    def __init__(self,conn: conn.Conn, blank:bool=True) -> None:
        self.conn = conn
        # deselect everything
        conn.bpy.ops.object.select_all(action="DESELECT")
        if blank:
            try:
                self.remove_cube()
            except KeyError:
                pass

        # set num frames to 1
        self.conn.bpy.context.scene.frame_end=1
        self.conn.bpy.context.scene.frame_start = 0
    
    def remove_cube(self):
        # select cube
        cube = self.conn.bpy.data.objects["Cube"]
        # delete it
        # https://blender.stackexchange.com/questions/27234/python-how-to-completely-remove-an-object
        cube.select_set(True)
        self.conn.bpy.ops.object.delete(True)


    def render(self,img_name,local_render_path, format):
        bpy = self.conn.bpy
        if format=="JPEG" or format=="PNG":
            file_path = os.getcwd()
            out_path = file_path + f"/{local_render_path}/renders/{img_name}.{format.lower()}"
            bpy.context.scene.render.filepath = out_path
            bpy.context.scene.render.threads=4
            bpy.context.scene.render.image_settings.file_format = format
            bpy.ops.render.render(write_still=True)

        else:
            print("format must be JPEG or PNG")

    def render_anim(self,anim_name,local_render_path):
        bpy = self.conn.bpy
        file_path = os.getcwd()
        out_path = file_path + f"/{local_render_path}/renders/{anim_name}"
        bpy.context.scene.render.filepath = out_path
        bpy.context.scene.render.threads=4
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.ops.render.render(animation=True,write_still=True)

    def get_camera(self):
        bpy = self.conn.bpy

        return bpy.data.objects["Camera"]
    
    def animate_camera(self,frames, pos= None,orientation=None,track_object=None):
        bpy = self.conn.bpy
        camera_obj = self.get_camera()
        if isinstance(track_object,AnimatedObject):
            const = camera_obj.constraints.new("TRACK_TO")
            const.target = track_object.instance

        elif len(orientation)>0:
            for o_i,f_i in zip(orientation,frames):
                o_i = self.conn.mathutils.Euler(o_i)
                camera_obj.rotation_euler = o_i
                camera_obj.keyframe_insert("rotation_euler", frame=f_i)

        if len(pos)>0:
            for (p_i,f_i) in zip(pos,frames):
                camera_obj.location = p_i
                camera_obj.keyframe_insert("location",frame = f_i)
