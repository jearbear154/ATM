from networkx.classes.graph import Graph

"""
TreeConverter --- class to perform the conversion from an ATM proof-tree to the graphical representation of the tree
:author Jeremy McMahan
"""


class TreeConverter:
    """
    Constructs the graphical representation of the proof-tree from the computation tree
    :param T the ComputationTree
    :returns the graphical representation of the proof-tree
    """
    @staticmethod
    def to_graphics(T):
        G = Graph()
        TreeConverter.to_nx_graph(T.proof_tree(), G, 1)
        return G

    """
    Adds a subtree of a proof-tree into the networkx graph and uses the number given as the root's name 
    :param T a subtree of a proof-tree
    :param G a networkx graph
    :param name the name to be given to the root of T
    :returns the next free name that can be used for a vertex
    """
    @staticmethod
    def to_nx_graph(T, G, name):
        G.add_node(name, label=T.root[0])  # enable many nodes to have same name when displayed
        next_name = name+1
        for child in T.children:
            current_name = next_name
            next_name = TreeConverter.to_nx_graph(child, G, current_name)
            G.add_edge(name, current_name, label=T.root[1])  # display the character read on the edge
        return next_name
