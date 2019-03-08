from networkx.classes.multidigraph import MultiDiGraph
from converter.atm_graph import ATMGraph

"""
GraphConverter --- class to perform the conversion between the graphical representation of an ATM and the 
specialized multi-graph representation of an ATM
:author Jeremy McMahan
"""


class GraphConverter:
    """
    Constructs the graphical representation of the ATM represented by the specialized multi-graph representation
    :param A the ATMGraph representation of an ATM
    :returns the graphical representation of the ATM
    """
    @staticmethod
    def to_graphics(A):
        G = MultiDiGraph()
        G.add_nodes_from(A.vertices())
        for u, v in A.edges():
            for a, b, d in A.weights(u, v):
                G.add_edge(u, v, label=a + "->" + b + "," + d)
        return G

    """
    Constructs the specialized multi-graph representation of the ATM represented in the graphical representation 
    :param states_and_types a set of strings of form q,t where q is a state and t is its type
    :param Sigma the input alphabet
    :param left_end the left end marker
    :param start the start state
    :param delta a dictionary of form delta[(p,q)] = a set of strings of form a->b,d representing the transition 
    delta(p,a) = {(q,b,d),...}
    :returns the ATMGraph representation of the ATM represented in the graphical representation
    """
    @staticmethod
    def from_graphics(states_and_types, Sigma, left_end, blank, start, delta):
        A = ATMGraph(Sigma, left_end, blank, start, None)
        types = {}
        for s in states_and_types:  # construct states and types
            q, t = s.rsplit(',', 1)
            types[q] = t
            A.add_vertex(q)

        def t(q):
            return types[q]
        A.t = t

        for p, q in delta:           # construct transitions
            for s in delta[(p, q)]:
                a, r = s.split("->", 1)
                b, d = r.rsplit(',', 1)
                A.add_edge(p, q, (a, b, d))

        return A
