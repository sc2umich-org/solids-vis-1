from dotenv import load_dotenv
import os
import bpy
load_dotenv()
path = os.environ.get("BLENDER_PATH")
class B_Connect():
    def __init__(self,path):
        self.path = path
        # bpy.app.binary_path = path
        # connect to blender


if __name__=="__main__":
    path = os.environ.get("BLENDER_PATH")
    con = B_Connect(path)
    bpy.context.scene.render.filepath = r"C:\Users\Jacob\projects\solids_vis\test.png"
    bpy.context.scene.render.image_settings.file_format = "jpeg"
    bpy.ops.render.render(write_still=True)