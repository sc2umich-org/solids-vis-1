import numpy as np
import solid_vis.objectmesh as objm
import solid_vis.conn as conn
from solid_vis.Scene import Scene
from solid_vis.AnimatedObject import AnimatedObject
import bpy

pn = 400
l1 = 300
l2 = 200
h = 3000
thickness = 13    
class CollapseWall():
    def __init__(self,pn,l1,l2,h,thickness):
        a = l1/2
        c = l2
        b = np.sqrt(c**2-a**2)

        t_p = thickness*a/c
        depth = 3*thickness+t_p+b
        gap = thickness*b/c
        gap_p = (thickness+t_p)*a/b
        long_length = a+gap*2+gap_p+pn
        diag_extension = thickness*a/b
        diag_len = (thickness+t_p)*c/b+c-thickness*a/b
        angle = np.arccos(a/c)*180/np.pi
        shift = (diag_len+diag_extension)*a/c+thickness*c/(2*b)

        panels = [
            {
                "name":"ec_left",
                "width":depth,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,90],
                "translation":[thickness,0,0],
            },
            {
                "name":"ec_right",
                "width":depth,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,90],
                "translation":[
                    thickness+long_length+pn+2*gap+thickness,
                    0,
                    0
                ],
            },
            {
                "name":"l2acc_lo",
                "width":l2,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,angle],
                "translation":[
                    pn-a+gap+thickness,
                    thickness*2,
                    0
                ],
            },
            {
                "name":"l2acc_li",
                "width":l2,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,180-angle],
                "translation":[
                    pn+gap+a+thickness*b/c+thickness,
                    thickness*2+thickness*a/c,
                    0
                ],
            },
            {
                "name":"l2acc_ri",
                "width":l2,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,180-angle],
                "translation":[
                    long_length+thickness*b/c+thickness,
                    thickness+thickness*a/c,
                    0
                ],
            },
            {
                "name":"l2acc_ro",
                "width":l2,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,angle],
                "translation":[
                    thickness+long_length+gap*2,
                    thickness,
                    0
                ],
            },
            {
                "name":"l1acc_left",
                "width":l1,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    pn+gap-a+thickness,
                    thickness,
                    0
                ],
            },
            {
                "name":"l1acc_right",
                "width":l1,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    pn+gap*3+gap_p+thickness,
                    depth-thickness*2,
                    0
                ],
            },
            {
                "name":"pn_left",
                "width":pn,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    thickness,
                    depth-thickness,
                    0
                ],
            },
            {
                "name":"pn_right",
                "width":pn,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    thickness+long_length+gap*2,
                    0,
                    0
                ],
            },
            {
                "name":"pl_left",
                "width":long_length,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    thickness,
                    0,
                    0
                ],
            },
            {
                "name":"pl_right",
                "width":long_length,
                "height":h,
                "thickness":thickness,
                "rotation":[90,0,0],
                "translation":[
                    thickness+pn+gap*2,
                    depth-thickness,
                    0
                ],
            },

        ]
        bpy_conn = conn.Conn()


        # left diag
        translation = [long_length-(gap+gap_p+a)*2+thickness,thickness,0]
        rotation = [0,0,angle]
        translation = [t/1000 for t in translation]
        mesh = objm.FeatureMesh("diag_left")
        var1 = mesh.sketch_plane(
            [
                [0,0,0],
                [-diag_extension/1000,thickness/1000,0],
                [diag_len/1000,thickness/1000,0],
                [(diag_len+diag_extension)/1000,0,0],
            ],
            [[0,1,2,3]]
        )
        mesh.extrude_plane(var1["face"][0],1,h/1000)
        mesh.place_object(translation,rotation)
        mesh.save_mesh()
        ec_obj =  AnimatedObject(bpy_conn,[],mesh,mesh.name)
        # should make a new collection to keep organized with multiple walls
        bpy_conn.bpy.context.collection.objects.link(ec_obj.instance)
        ec_obj.instance.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        ec_obj.instance.select_set(False)
        
        
        # right diag
        translation = [long_length+(gap)*2+thickness+thickness*c/b,thickness,0]
        rotation = [0,0,angle]
        translation = [t/1000 for t in translation]
        mesh = objm.FeatureMesh("diag_left")
        var1 = mesh.sketch_plane(
            [
                [0,0,0],
                [-diag_extension/1000,thickness/1000,0],
                [diag_len/1000,thickness/1000,0],
                [(diag_len+diag_extension)/1000,0,0],
            ],
            [[0,1,2,3]]
        )
        mesh.extrude_plane(var1["face"][0],1,h/1000)
        mesh.place_object(translation,rotation)
        mesh.save_mesh()
        ec_obj =  AnimatedObject(bpy_conn,[],mesh,mesh.name)
        # should make a new collection to keep organized with multiple walls
        bpy_conn.bpy.context.collection.objects.link(ec_obj.instance)
        ec_obj.instance.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        ec_obj.instance.select_set(False)

        for p in panels:
            thickness = p["thickness"]/1000
            width = p["width"]/1000
            height = p["height"]/1000
            translation = [t/1000 for t in p["translation"]]
            mesh = objm.FeatureMesh(p["name"])
            var1 = mesh.add_plane(height,width)
            print(var1)
            mesh.extrude_plane(var1["face"][0],1,thickness)
            mesh.place_object(translation,p["rotation"])
            mesh.save_mesh()
            ec_obj =  AnimatedObject(bpy_conn,[],mesh,mesh.name)
            # should make a new collection to keep organized with multiple walls
            bpy_conn.bpy.context.collection.objects.link(ec_obj.instance)
            ec_obj.instance.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            ec_obj.instance.select_set(False)

        scene = Scene(bpy_conn)
        bpy_conn.save_blend("examples/blend/plate_wall.blend")
        

CollapseWall(pn,l1,l2,h,thickness)




#     acc_left_inn = parts["inn_acc"].assemble(assembly,"li",[-90,angle,180],[nominal_length-a+gap+len_1,height,b+thickness+t_p])

#     draw_l2_hinge(parts["inn_acc"],hinge_params,acc_left_inn,"li",assembly)

#     acc_right_inn = parts["inn_acc"].assemble(assembly,"ri",[-90,angle,180],[nominal_length-a+gap+len_1+gap+gap_p,height,b+thickness+t_p+thickness])

#     draw_l2_hinge(parts["inn_acc"],hinge_params,acc_right_inn,"ri",assembly)

#     acc_right_out = parts["inn_acc"].assemble(assembly,"ro",[-90,angle,0],[nominal_length-a+gap+len_1+gap+gap_p+2*gap,0,b+thickness+t_p+thickness])

#     draw_l2_hinge(parts["inn_acc"],hinge_params,acc_right_out,"ro",assembly)

#     nom_left = parts["pn"].assemble(assembly,"nom_left",[-90,0,0],[0,0,thickness])

#     draw_nom_hinge(parts["pn"],hinge_params,nom_left,"left")

#     nom_right = parts["pn"].assemble(assembly,"nom_right",[-90,180,0],[nominal_length+long_length+gap*2,0,depth-thickness])

#     draw_nom_hinge(parts["pn"],hinge_params,nom_right,"nom_right")

#     flat_acc_left = parts["acc"].assemble(assembly,"acc_left",[-90,0,0],[nominal_length+gap*3+gap_p,0,thickness*2])

#     draw_nom_hinge(parts["acc"],hinge_params,flat_acc_left,"left")

#     flat_acc_right = parts["acc"].assemble(assembly,"acc_right",[-90,180,0],[long_length-gap-gap_p,0,depth-thickness*2])

#     draw_nom_hinge(parts["acc"],hinge_params,flat_acc_right,"right")

#     long_left = parts["pl"].assemble(assembly,"long_left",[-90,0,0],[nominal_length+gap*2,0,thickness])

#     draw_long_hinge(parts["pl"],hinge_params,long_left,"left")

#     long_right = parts["pl"].assemble(assembly,"long_right",[-90,180,0],[long_length,0,depth-thickness])

#     draw_long_hinge(parts["pl"],hinge_params,long_right,"right")




