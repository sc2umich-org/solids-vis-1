import numpy as np
import bpy
import finite_elem_lib.gen_mesh as gen_mesh
import time
class Node_3():
    id = 0
    def __init__(
            self, 
            position,
            neighbors = None,
            id = 0,
            _neighbors = None,
            _id = 0,
            x_fixity = False,y_fixity = False, z_fixity = False,
            x_load   = 0,      y_load = 0,       z_load = 0,
            x_disp   = 0,      y_disp = 0,       z_disp = 0
        ):
        '''
        A 3 dimension node. Can be x,y,z or x,y,rotation. 

        id: A global id that was defined by the user
        
        neighbors: a list containing global id's, defined by the user, of the
        nodes this node is connected to. This array is defined by the user

        _id: a modified verson of the global id that is made amenable to python
        idexing. 

        _neighbors: a list that is parallel to neighbors but contains the 
        modified version of id's that are amenable to python indexing. This is
        used to create connectivity matrices.

        fixities: defines a fixed condition

        loads: defines loads

        disps: defines any displacement on the nodes
        '''

        self.relevant_DOF = [bool(i) for i in [1,1,1]]

        self.id = id
        self._id = _id

        if neighbors is None:
            self.neighbors = []
        else:
            self.neighbors = neighbors

        if _neighbors is None:   
            self._neighbors = []
        else:
            self._neighbors = _neighbors

        self.position = np.array(position)

        # THese lists have to be converted to np arrays to support boolean mask
        # indexing.
        self.fixity = np.array([
            int(x_fixity),
            int(y_fixity),
            int(z_fixity)
        ])

        self.loading = np.array([
            x_load,
            y_load,
            z_load
        ])

        self.disp    = np.array([
            x_disp,
            y_disp,
            z_disp
        ])

    def __repr__(self):
        return f'{self.id}'
node_pos = [
    [0,0,0],
    [0,1,0],
    [0,0,1],
    [0,1,1],
    [1,0,0],
    [1,1,0],
    [1,0,1],
    [1,1,1],
]
nodes = []
for n_pos in node_pos:
    nodes.append(Node_3(n_pos))

meshed_nodes = []
while nodes:
    for node in nodes:

        if len(meshed_nodes)>2:
            for i in reversed(range(2,len(meshed_nodes))):
                a =meshed_nodes[i].position-node.position
                b =meshed_nodes[i-1].position-node.position
                c =meshed_nodes[i-2].position-node.position
                abc_matrix = np.array([a,b,c])
                if np.linalg.det(abc_matrix)!=0:
                    nodes.remove(node)
                    node.id=Node_3.id
                    Node_3.id+=1
                    for m_node in meshed_nodes[i-2:i+1]:
                        m_node.neighbors.append(node.id)
                        node.neighbors.append(m_node.id)
                    node.neighbors.append(node.id)
                    meshed_nodes.append(node)
                    break

        if len(meshed_nodes)==2:
            a =meshed_nodes[0].position-meshed_nodes[1].position
            b =meshed_nodes[0].position-node.position
            if np.dot(a,b)>=1e-8:
                meshed_nodes.append(node)
                nodes.remove(node)
                node.id=Node_3.id
                Node_3.id+=1
                for m_node in meshed_nodes:
                    if not (node.id in m_node.neighbors):
                        m_node.neighbors.append(node.id)
                    if not (m_node.id in node.neighbors):
                        node.neighbors.append(m_node.id)

        if len(meshed_nodes)<2:
            meshed_nodes.append(node)
            nodes.remove(node)
            node.id=Node_3.id
            Node_3.id+=1
            for m_node in meshed_nodes:
                if not (node.id in m_node.neighbors):
                    m_node.neighbors.append(node.id)
                if not (m_node.id in node.neighbors):
                    node.neighbors.append(m_node.id)

conn_matrix = []
for node in meshed_nodes:
    conn_row = []
    for i in range(len(meshed_nodes)):
        if i in node.neighbors:
            conn_row.append(1)
        else:
            conn_row.append(0)
    conn_matrix.append(conn_row)
conn_matrix=np.array(conn_matrix)

edges = []
for i, row in enumerate(conn_matrix):
    for j in range(i+1,len(meshed_nodes)):
        if row[j]==1:
            edges.append((i,j))

faces = []
for i,edge_i in enumerate(edges):
    for j,edge_j in enumerate(edges):
        for k,edge_k in enumerate(edges):
            if i!=j and k!=j:
                cond1 = (edge_i[0]in edge_j or edge_i[0] in edge_k)and (edge_i[1]in edge_j or edge_i[1] in edge_k)
                cond2 = (edge_j[0]in edge_k or edge_j[0] in edge_i)and (edge_j[1]in edge_k or edge_i[1] in edge_i)
                cond3 = (edge_k[0]in edge_j or edge_k[0] in edge_i)and (edge_k[1]in edge_j or edge_i[1] in edge_i)
                v1 = np.cross(meshed_nodes[edge_i[1]].position-meshed_nodes[edge_i[0]].position,meshed_nodes[edge_j[1]].position-meshed_nodes[edge_j[0]].position)
                v2 = np.cross(meshed_nodes[edge_i[1]].position-meshed_nodes[edge_i[0]].position,meshed_nodes[edge_k[1]].position-meshed_nodes[edge_k[0]].position)
                sum1 = np.sum(v1-v2)
                sum2 = np.sum(v1+v2)
                if sum1<1e-6 or sum2<1e-6:
                    if cond1 and cond2 and cond3:
                        verts = np.unique(np.array([edge_i[0],edge_j[0],edge_k[0],edge_i[1],edge_j[1],edge_k[1]]))
                        faces.append(verts)
nodes = [meshed_nodes[i].position for i in range(8)]

mesh_data = bpy.data.meshes.new("ori")
mesh_data.from_pydata(nodes,edges,faces)
obj = bpy.data.objects.new('ori_obj',mesh_data)
bpy.context.collection.objects.link(obj)




    
        

    

def insert_keyframe(fcurves, frame, values):
    for fcu, val in zip(fcurves, values):
        fcu.keyframe_points.insert(frame, val, options={'FAST'})


# action = bpy.data.actions.new("MeshAnimation")
# fold.mesh.animation_data_create()
# fold.mesh.animation_data.action = action
# data_path = "vertices[%d].co"
# fcurve_list = []
# for v in fold.mesh.vertices:
#     fcurves = [action.fcurves.new(f"vertices[{v.index}].co", index =  i) for i in range(3)]
#     fcurve_list.append(fcurves)
# for t in range(100):
#     fold.update_verts()
#     for i,v in enumerate(fold.mesh.vertices):
#         print(v.index)
#         insert_keyframe(fcurve_list[i],t,v.co)
    
