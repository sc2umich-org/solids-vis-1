import bpy
import bmesh
import mathutils
from math import radians
import numpy as np
class FeatureMesh():
    def __init__(self,name):
        self.name = name
        me = bpy.data.meshes.new(name)
        self.bpy_mesh = me
        self.bmesh = bmesh.new()
        self.bmesh.from_mesh(me)


    def sketch_plane(self,in_verts,in_faces):
        verts = []
        for v in in_verts:
            vert = self.bmesh.verts.new(v)
            verts.append(vert)
        verts = np.array(verts)
        faces = []
        for f in in_faces:
            print(verts)
            face = self.bmesh.faces.new(verts[f])
            faces.append(face)
        return {"verts":verts,"face":faces}
    def add_plane(self,height,width):
        # going to have to go directly into bmesh to have fine control over meshes 
        mat1 = mathutils.Matrix.Translation((width/2,height/2,0))
        mat2 = mathutils.Matrix.Scale(height/width,4,[0,1,0])
        
        new_area = bmesh.ops.create_grid(self.bmesh,size = width/2,matrix = mat1@mat2)
        # I need a way to find the face associated with this op
        new_area["face"]=new_area["verts"][0].link_faces
        return new_area
    
    def extrude_plane(self,face,dir,magnitude):
        face.normal_update()
        new_area = bmesh.ops.extrude_face_region(self.bmesh,geom=[face])
        mat1 = mathutils.Matrix.Translation(face.normal*dir*magnitude)
 

        verts = []
        for g in new_area["geom"]:
            if isinstance(g,bmesh.types.BMVert):
                verts.append(g)
        bmesh.ops.transform(self.bmesh,matrix = mat1,verts = verts)

    def place_object(self, translation,rotation):
        verts = self.bmesh.verts
        mat1 = mathutils.Matrix.Translation(translation)
        mat2 = mathutils.Matrix.Rotation(radians(rotation[0]), 4, 'X')
        mat3 = mathutils.Matrix.Rotation(radians(rotation[1]), 4, 'Y')
        mat4 = mathutils.Matrix.Rotation(radians(rotation[2]), 4, 'Z')
        mat_rot = mat4@mat3@mat2
        bmesh.ops.rotate(self.bmesh,cent = [0,0,0], matrix = mat_rot, verts = verts)
        bmesh.ops.transform(self.bmesh,matrix = mat1,verts = verts)

        

    def save_mesh(self):
        # this should only be called if all changes have been made.
        self.bmesh.to_mesh(self.bpy_mesh)
        self.bmesh.free()



        