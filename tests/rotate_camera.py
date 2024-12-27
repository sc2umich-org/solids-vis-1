import numpy as np
import sys
from solid_vis.conn import Conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
sys.path.append('.')



if __name__=="__main__":

    motion_data = np.array([[x,0,0] for x in np.arange(-10,10,1)])
    motion_data_2 = np.array([[0,0,0] for x in np.arange(-10,10,1)])
    camera_pos = np.array([[0,0,-5] for x in np.arange(-10,10,1)])
    camera_angle = np.array([[0,0,0] for zr in np.arange(45*np.pi/180,-45*np.pi/180,-90/20*np.pi/180)])
    print(camera_angle)
    frames = [x for x in range(20)]
    bpy_conn = Conn()
    scene = Scene(bpy_conn)
    obj = AnimatedObject(
        bpy_conn,
        motion_data,
        "uv_sphere",
        "test_sphere",
    )
    obj = AnimatedObject(
        bpy_conn,
        motion_data_2,
        "uv_sphere",
        "stationary",
    )
    scene.animate_camera(camera_pos,camera_angle,frames)
    scene.render_anim("rotate_cam","tests")