import numpy as np
import sys
sys.path.append('.')
import sv



if __name__=="__main__":

    motion_data = np.array([[x,0,0] for x in np.arange(-10,10,1)])
    bpy_conn = sv.conn.Conn()
    scene = sv.Scene.Scene(bpy_conn)
    obj = sv.AnimatedObject.AnimatedObject(
        bpy_conn,
        motion_data,
        "uv_sphere",
        "test_sphere",
    )

    scene.render("added sphere","tests", "JPEG")