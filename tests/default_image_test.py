import bpy
import os

def def_img_test(format):
    if format=="JPEG" or format=="PNG":
        file_path = os.path.dirname(__file__)
        out_path = file_path + f"/renders/test.{format.lower()}"
        bpy.context.scene.render.filepath = out_path
        bpy.context.scene.render.image_settings.file_format = format
        bpy.ops.render.render(write_still=True)

    else:
        print("format must be JPEG or PNG")


if __name__=="__main__":
    def_img_test("JPEG")