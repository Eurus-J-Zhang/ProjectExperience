from submission import construct_probability_table
import numpy as np

# Bayes network construction
class bayes_network:
    def __init__(self, data):
        self.nodes = []
        self.roots = []
        self.data = data

    def get_node(self, feature):
        res = [node for node in self.nodes if node.data_id == feature]
        return res[0] if len(res) == 1 else None

    # Method to get P(feature | conditions)
    def get_node_probability(self, feature, conditions):
        # Inputs: 
        #       - feature : node_id for the query
        #       - condititions : 1xD dictionary of (B : val_B, ..., Z : val_Z) pairs 
        Node = self.get_node(feature)
        tmp = {}

        # Get rid of excess parent-conditions
        for key in conditions.keys():
            if key in Node.parents:
                tmp[key] = conditions[key]
        
        # We can only evaluate node which has assignment to all of it's parents
        assert len(tmp) == len(Node.parents), "Not all parents of a node have a value"

        # Make a key
        dict_key = "vals" # + str(B)
        dict_key += "".join([".{}:{}.".format(key, tmp[key]) for key in sorted(tmp.keys())])
        return Node.probabilities[dict_key]

    def append_node(self, node_id, name, parents = []):
        Node = node(name, node_id)
        Node.probabilities = construct_probability_table(self.data, node_id, parents)

        Node.parents = parents
        self.nodes.append(Node)
        if parents != []:
            for parent in parents:
                res = self.get_node(parent)
                assert res != None
                res.children.append(Node)
        else:
            self.roots.append(Node)


# A node in Bayes network
class node:
    def __init__(self, name, node_id):
        self.name = name
        self.data_id = node_id
        self.probabilities = []
        self.parents = []
        self.children = []

    def add_parent(self, parent):
        self.parents.append(parent)
        
    def add_child(self, child):
        self.children.append(child)


