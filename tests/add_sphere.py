
import sys
sys.path.append('.')
import sv



if __name__=="__main__":
    bpy_conn = sv.conn.Conn()
    scene = sv.Scene.Scene(bpy_conn)
    obj = sv.AnimatedObject.AnimatedObject(
        bpy_conn,
        [[0,0,0]],
        "uv_sphere",
        "test_sphere",
    )

    scene.render("added sphere","tests", "JPEG")