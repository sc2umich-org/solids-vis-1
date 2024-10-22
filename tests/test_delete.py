import sys
sys.path.append('.')
import sv

if __name__=="__main__":
    bpy_conn = sv.conn.Conn()
    scene = sv.Scene.Scene(bpy_conn,True)
    scene.render("default","tests", "JPEG")