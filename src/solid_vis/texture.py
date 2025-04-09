import bpy
class Texture():
    def __init__(self,name,graph):
        mat = bpy.data.materials.new(name)
        self.mat = mat
        mat.use_nodes = True
        self.nodes = mat.node_tree.nodes
        self.links = mat.node_tree.links
        self.node_ledger = [0]*len(graph)
        # set use nodes to true 

        root = self.nodes.get('Material Output')
        print(root)
        for node in graph:
            new_node = self.nodes.new(node["node_type"])
            self.node_ledger[node["id"]]=new_node
            for k,v in node["args"].items():
                setattr(new_node,k,v)

            # connections from the output of this node to inputs of another node
            for connection in node["connections"]:
                # what if node doesn't exist when connection attempt is made
                if connection["id"]==-1:
                    other = root
                else:
                    other = self.node_ledger[connection["id"]]
                if isinstance(other,int):
                    print("nodes are defined in the wrong order, texture is broken")
                    raise IndexError
                    
                self.links.new(
                    other.inputs[connection["inp"]],
                    new_node.outputs[connection["out"]]
                )




# example tree
# Surface, Volume, Displacement, and Thickness are all good values for parent
# input.
t = [{
    "output":"BSDF",
    "parent_input":"Surface",
    "node_type":"BsdfPrincipled",
    "args":{

    },
    "children":[
        {
            "node_type": "LinearLight", # node.bl_idname
            "args":{},
            "output":"Mix (Legacy)",
            "parent_input":"Vector"
        }
    ]
}]

