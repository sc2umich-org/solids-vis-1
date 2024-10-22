import finite_elem_lib.gen_mesh as gen_mesh
import numpy as np

# Define Nodes

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
    nodes.append(gen_mesh.Node_3(n_pos))

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
                    node.id=gen_mesh.Node_3.id
                    gen_mesh.Node_3.id+=1
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
                node.id=gen_mesh.Node_3.id
                gen_mesh.Node_3.id+=1
                for m_node in meshed_nodes:
                    if not (node.id in m_node.neighbors):
                        m_node.neighbors.append(node.id)
                    if not (m_node.id in node.neighbors):
                        node.neighbors.append(m_node.id)

        if len(meshed_nodes)<2:
            meshed_nodes.append(node)
            nodes.remove(node)
            node.id=gen_mesh.Node_3.id
            gen_mesh.Node_3.id+=1
            for m_node in meshed_nodes:
                if not (node.id in m_node.neighbors):
                    m_node.neighbors.append(node.id)
                if not (m_node.id in node.neighbors):
                    node.neighbors.append(m_node.id)


other_nodes = [
    [0,2,0],
    [0,2,1],
    [1,1,0],
    [1,1,1],
    [1,2,0],
    [1,2,1],
]