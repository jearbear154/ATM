from simulator.atm import ATM
from converter.atm_graph import ATMGraph
from converter.multigraph import MultiGraph

"""
ATMConverter --- class that performs the conversions between an ATM and the directed multi-graph representation of an ATM
:author Jeremy McMahan
"""


class ATMConverter:
    """
    Creates the multi-graph representation of the given ATM
    :param M the ATM
    :returns the multi-graph representation of M
    """
    @staticmethod
    def to_graph(M):
        G = ATMGraph(M.Sigma, M.left_end, M.blank, M.start, M.t)

        for q in M.Q:
            G.add_vertex(q)

        for q in M.Q:
            for a in M.Gamma:
                for p, b, d in M.delta(q, a):
                    G.add_edge(q, p, (a, b, d))

        return G

    """
    Creates the ATM represented by the given multi-graph
    :param A the multi-graph representation
    :returns the ATM represented by A
    """
    @staticmethod
    def from_graph(A):
        transitions = dict()
        Gamma = set(A.Sigma)

        for u, v in A.edges():
            for a, b, d in A.weights(u, v):
                if (u, a) not in transitions:
                    transitions[(u, a)] = set()
                transitions[(u, a)] |= {(v, b, d)}  # make transitions
                Gamma |= {b}                        # make tape alphabet

        def delta(q, a):
            return set() if (q, a) not in transitions else transitions[(q, a)]

        return ATM(set(A.vertices()), A.Sigma, Gamma, A.left_end, A.blank, delta, A.start, A.t)
