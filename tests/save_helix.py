import numpy as np
import sys
from solid_vis.conn import Conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
sys.path.append('.')



if __name__=="__main__":
    
    motion_data = np.array([[5*np.cos(x),x,5*np.sin(x)+5] for x in np.arange(-10,10,.1)])
    frames = [0,199]
    positions = [
        [10,-10,5],
        [10,20,30],
    ]
    bpy_conn = Conn()
    scene = Scene(bpy_conn)
    obj = AnimatedObject(
        bpy_conn,
        motion_data,
        "uv_sphere",
        "test_sphere",
    )
    scene.animate_camera(frames,pos=positions,track_object=obj)
    bpy_conn.save_blend("tests/blend/helix.blend")