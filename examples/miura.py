import numpy as np
import bpy
import time

def get_f(thetas,rhos,dt=True,j=None):
    b_mats = []
    c_mats = []
    x_mats = []
    f_mat = np.identity(3)
    for i,(t,r) in enumerate(zip(thetas,rhos)):
        c = np.cos(np.deg2rad(t))
        s = np.sin(np.deg2rad(t))
        b = [
            [c,-s,0],
            [s,c,0],
            [0,0,1],
        ]
        b_mats.append(b)
        if dt and i==j:
            c = -np.sin(np.deg2rad(r))
            s = np.cos(np.deg2rad(r))
            con = 0
        else:
            c = np.cos(np.deg2rad(r))
            s = np.sin(np.deg2rad(r))
            con = 1
        c_mat = [
            [con,0,0],
            [0,c,-s],
            [0,s,c],
        ]
        c_mats.append(c_mat)
        x_mats.append(np.matmul(c_mat,b))
        f_mat = np.matmul(f_mat,np.matmul(c_mat,b))
    if dt:
        return f_mat
    else:
        return x_mats

def get_base(thetas, rhos):
    dfs = []
    for j,rho in enumerate(rhos):
        df = np.reshape(get_f(thetas,rhos,True,j),(-1,1))
        dfs.append(df)
    c = np.column_stack(dfs)
    orthogonal_base = np.identity(len(rhos))-np.matmul(np.linalg.pinv(c),c)
    return orthogonal_base

class folds():
    def __init__(self,thetas,rot_vec) -> None:
        self.thetas = thetas
        self.rot_vec = rot_vec

        self.verts = [
            [0,0,0]
        ]
        #need this to create an origami object
        self.generate_verts()

        mesh_data = bpy.data.meshes.new("ori")
        mesh_data.from_pydata(self.verts,[],self.faces)
        obj = bpy.data.objects.new('ori_obj',mesh_data)
        bpy.context.collection.objects.link(obj)
        self.mesh = mesh_data
        self.obj=obj

    def update_rot(self):
        d_rot = np.array([1/100*90,1/100*90,1/100*90,-2/100*90,1/100*90])
        orthogonal_base = get_base(self.thetas, self.rot_vec)
        self.rot_vec = self.rot_vec + np.matmul(orthogonal_base,d_rot)
        # print(self.rot_vec)
    
    def generate_verts(self):
        faces = []
        for i in range(len(self.thetas)):
            faces.append([0])
        x_mats = get_f(self.thetas, self.rot_vec, False)
        fold_lines = np.array([[1,0,0]])
        transfrom = np.identity(3)
        for i,x in enumerate(x_mats):
            transfrom = np.matmul(transfrom,x)
            result = np.matmul(transfrom,fold_lines[0,:,None])
            fold_lines= np.concatenate((fold_lines,[result[:,0]]),axis=0)
            self.verts.append(list(result[:,0]))
            faces[i].append(i+1)
            faces[i-1].append(i+1)
        self.faces = faces

    def update_verts(self):
        self.update_rot()
        self.generate_verts()
        x_mats = get_f(self.thetas, self.rot_vec, False)
        fold_lines = np.array([[1,0,0]])
        transfrom = np.identity(3)
        for i,x in enumerate(x_mats):
            transfrom = np.matmul(transfrom,x)
            result = np.matmul(transfrom,fold_lines[0,:,None])
            self.mesh.vertices[i+1].co = list(result[:,0])
        


def plot_vec(thetas,rot_vec,lines=None):
    if lines ==None:
        lines_new = []
    fold_lines = np.array([[1,0,0]])
    result = fold_lines[0,:,None]
    x_mats = get_f(thetas, rot_vec, False)
    transfrom = np.identity(3)
    if lines ==None:
        line = ax.quiver(0, 0, 0, result[0,0], result[1,0], result[2,0], color='purple', arrow_length_ratio=0.1)
        lines_new.append(line)
    else:
        seg = lines[0]._segments3d
        seg[0][0]=result[:,0]
        lines[0].set_segments(seg)
    for i,(x,color) in enumerate(zip(x_mats,['r','b','g','y','k'])):
        transfrom = np.matmul(transfrom,x)
        result = np.matmul(transfrom,fold_lines[0,:,None])
        fold_lines= np.concatenate((fold_lines,[result[:,0]]),axis=0)
        if lines ==None:
            line = ax.quiver(0, 0, 0, result[0,0], result[1,0], result[2,0], color=color, arrow_length_ratio=0.1)
            lines_new.append(line)
        else:
            seg = lines[i+1]._segments3d
            seg[0][0]=result[:,0]
            lines[i+1].set_segments(seg)
    if lines == None:
        return lines_new
    else: 
        return lines
    

def insert_keyframe(fcurves, frame, values):
    for fcu, val in zip(fcurves, values):
        fcu.keyframe_points.insert(frame, val, options={'FAST'})

thetas = np.array([90,90,45,45,90])
rot_vec = np.array([0,0,0,0,0])
fold = folds(thetas,rot_vec)
action = bpy.data.actions.new("MeshAnimation")
fold.mesh.animation_data_create()
fold.mesh.animation_data.action = action
data_path = "vertices[%d].co"
fcurve_list = []
for v in fold.mesh.vertices:
    fcurves = [action.fcurves.new(f"vertices[{v.index}].co", index =  i) for i in range(3)]
    fcurve_list.append(fcurves)
for t in range(100):
    fold.update_verts()
    for i,v in enumerate(fold.mesh.vertices):
        print(v.index)
        insert_keyframe(fcurve_list[i],t,v.co)
    
