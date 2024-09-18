import os
import sys
from sv.conn import Conn

def remove_cube():
    # select cube
    cube = Conn.bpy.data.objects["Cube"]
    # delete it
    # https://blender.stackexchange.com/questions/27234/python-how-to-completely-remove-an-object
    cube.select_set(True)
    Conn.bpy.ops.object.delete(True)

def render(img_name,local_render_path, format):
    if format=="JPEG" or format=="PNG":
        file_path = os.getcwd()
        out_path = file_path + f"/{local_render_path}/renders/{img_name}.{format.lower()}"
        Conn.bpy.context.scene.render.filepath = out_path
        Conn.bpy.context.scene.render.threads=4
        Conn.bpy.context.scene.render.image_settings.file_format = format
        Conn.bpy.ops.render.render(write_still=True)

    else:
        print("format must be JPEG or PNG")