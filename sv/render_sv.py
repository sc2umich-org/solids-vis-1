import os
from sv.conn import Conn

def render(img_name, format):
    if format=="JPEG" or format=="PNG":
        file_path = os.path.dirname(__file__)
        out_path = file_path + f"/renders/{img_name}.{format.lower()}"
        Conn.bpy.context.scene.render.filepath = out_path
        Conn.bpy.context.scene.render.threads=1
        Conn.bpy.context.scene.render.image_settings.file_format = format
        Conn.bpy.ops.render.render(write_still=True)

    else:
        print("format must be JPEG or PNG")