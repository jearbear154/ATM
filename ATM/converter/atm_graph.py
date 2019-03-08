from converter.multigraph import MultiGraph

"""
ATMGraph --- class that represents an Alternating Turing Machine as a multi-graph. Specifically, this graph has
specific attributes for the information of the ATM other than the transition function and states which are represented 
as a multi-graph. Furthermore, the multi-graph represents a transition delta(q,a) = (p, b, d) by having an edge q -> p 
with weight (a, b, d). Also, each state is a vertex of the graph. We assume any symbol on a transition not in the input
alphabet is in the tape alphabet.
:author Jeremy McMahan
"""


class ATMGraph(MultiGraph):
    """
    Creates the multi-graph representation of the ATM
    :param Sigma the input alphabet
    :param left_end the left end marker
    :param blank the blank symbol
    :param start the start state
    :param t the type function
    """

    def __init__(self, Sigma=set(), left_end='|-', blank=' ', start='q', t=lambda q: '∧'):
        MultiGraph.__init__(self)
        self.Sigma = Sigma
        self.left_end = left_end
        self.blank = blank
        self.start = start
        self.t = t

    """
    Determines if the two ATMGraphs are equal
    :param other the other ATMGraph
    :returns True iff the two ATMGraphs are equal
    """

    def __eq__(self, other):
        states_transitions_equal = MultiGraph.__eq__(self, other)
        input_alphabets_equal = self.Sigma == other.Sigma
        left_ends_equal = self.left_end == other.left_end
        blanks_equal = self.blank == other.blank
        starts_equal = self.start == other.start

        if not states_transitions_equal:
            return False
        else:
            for q in self.vertices():
                if self.t(q) != other.t(q):
                    return False
            return input_alphabets_equal and left_ends_equal and blanks_equal and starts_equal

    """
    Determines if the two ATMGraphs are not equal
    :param other the other ATMGraph
    :returns True iff the two ATMGraphs not are equal
    """

    def __ne__(self, other):
        return not (self == other)
