
import sys
sys.path.append('.')
import sv

primitive_obj_ids = ["torus","monkey","circle","plane","cone","cylinder","grid","ico_sphere"]
#primitive_obj_ids=["uv_sphere"]

if __name__=="__main__":
    for i_name in primitive_obj_ids:
        bpy_conn = sv.conn.Conn()
        scene = sv.Scene.Scene(bpy_conn)
        obj = sv.AnimatedObject.AnimatedObject(
            bpy_conn,
            [[0,0,0]],
            i_name,
            i_name+'1',
        )

        scene.render("added "+i_name,"tests", "JPEG")
        obj.delete_object()
        
    
    i_name='uv_sphere'
    bpy_conn = sv.conn.Conn()
    scene = sv.Scene.Scene(bpy_conn)
    obj = sv.AnimatedObject.AnimatedObject(
        bpy_conn,
        [[0,0,0]],
        i_name,
        i_name+'1',
        segments=128,
        radius=0.5,
        ring_count=32
    )

    scene.render("added "+i_name,"tests", "JPEG")
