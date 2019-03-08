
"""
Tree --- class to represent an accepting computation tree of an Alternating Turing Machine
:author Jeremy McMahan
"""


class Tree:
    """
    Creates the tree from the root data and a list of subtrees. A leaf is denoted by having the empty list
    as its children
    :param root the data associated with the tree's root
    :param children a list of trees to be the tree's subtrees
    """

    def __init__(self, root, children=[]):
        self.root = root
        self.children = children

    """
    Computes the depth of the Tree
    :returns the depth
    """

    def depth(self):
        if self.children == []:
            return 0
        else:
            return 1 + max([child.depth() for child in self.children])

    """
    Determines if the tree is equal to other_tree
    :param other_tree a tree
    :returns True iff this tree and other_tree are equal
    """

    def __eq__(self, other_tree):
        if other_tree is None or self.root != other_tree.root:
            return False
        else:
            if len(self.children) != len(other_tree.children):
                return False
            else:
                for i in range(len(self.children)):
                    if self.children[i] != other_tree.children[i]:
                        return False
                return True

    """
    Determines if the tree is not equal to other_tree
    :param other_tree a tree
    :returns True iff this tree and other_tree are not equal
    """

    def __ne__(self, other_tree):
        return not self == other_tree
