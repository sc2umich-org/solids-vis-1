import bpy
class Texture():
    def __init__(self,name,tree):
        mat = bpy.data.materials.new(name)
        self.mat = mat
        mat.use_nodes = True
        self.nodes = mat.node_tree.nodes
        self.links = mat.node_tree.links
        # set use nodes to true 

        root = self.nodes.get('Material Output')
        print(root)
        self.recurse_tree(tree,root)

    def recurse_tree(self,tree,parent):
        if tree=="":
            return
        for branch in tree:
            new_node = self.nodes.new(branch["node_type"])
            print(new_node.outputs[0])
            self.links.new(parent.inputs[branch["parent_input"]],new_node.outputs[branch["output"]])
            
            self.recurse_tree(branch.get("children",""),new_node)



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

