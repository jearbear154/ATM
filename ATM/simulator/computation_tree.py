from simulator.tree import Tree

"""
ComputationTree --- class to represent a computation tree, including functionality to get information about the 
computation
:author Jeremy McMahan
"""


class ComputationTree(Tree):
    """
    Computes the amount of time that the computation used
    :returns the time used in the computation
    """

    def time(self):
        return self.depth()

    """
    Computes the amount of space that the computation used
    :returns the space used in the computation
    """

    def space(self):
        if self.children == []:
            return len(self.root.tape) - 1  # don't include left end marker
        else:
            return max([len(self.root.tape) - 1, max([child.space() for child in self.children])])

    """
    Computes the tree of states and symbols read as the computation proceeded that proves the computation is accepting
    :returns the proof tree
    """

    def proof_tree(self):
        if self.children == []:
            return Tree((self.root.state, self.root.tape[self.root.head_position]))
        else:
            return Tree((self.root.state, self.root.tape[self.root.head_position]),
                        [child.proof_tree() for child in self.children])
