import numpy as np
import sys
from solid_vis.conn import Conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
sys.path.append('.')



if __name__=="__main__":

    motion_data = np.array([[x,0,0] for x in np.arange(-10,10,1)])
    bpy_conn = Conn()
    scene = Scene(bpy_conn)
    obj = AnimatedObject(
        bpy_conn,
        motion_data,
        "uv_sphere",
        "test_sphere",
    )

    scene.render_anim("moving sphere","tests")