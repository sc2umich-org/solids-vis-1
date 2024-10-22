import sv.conn as conn
import os

class Scene():
    def __init__(self,conn: conn.Conn, blank:bool=True) -> None:
        self.conn = conn
        # deselect everything
        conn.bpy.ops.object.select_all(action="DESELECT")
        self.remove_cube()

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