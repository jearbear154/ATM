from converter.atm_graph import ATMGraph
from converter.atm_converter import ATMConverter
from simulator.advanced_simulator import AdvancedSimulator
from graphics.tree_converter import TreeConverter
from graphics.graph_converter import GraphConverter

"""
Model --- represents the model of the program
:author Jeremy McMahan
"""


class Model:
    """
    Sets up the Model
    """

    def __init__(self):
        self.G = ATMGraph()  # the specialized multi-graph representation of the ATM
        self.t = dict()

    """
    Simulates the ATM on an input with time and space bounds
    :param x a list representing the input string to the machine
    :param T the time bound 
    :param S the space bound
    :returns time, space, and graphical representation of the proof tree if the computation accepted in the required
    time and space bounds and None otherwise
    """

    def simulate(self, x, T=None, S=None):
        A = ATMConverter.from_graph(self.G)
        tree = AdvancedSimulator.simulate(A, x, T, S)
        if tree is not None:
            return tree.time(), tree.space(), TreeConverter.to_graphics(tree)
        return None

    """
    Constructs the graphical representation of the ATM
    :returns the graphical representation of the ATM as a networkx graph
    """

    def graphical_representation(self):
        return GraphConverter.to_graphics(self.G)

    """
    Changes the blank symbol of the ATM
    :param blank the new blank symbol
    :returns None iff the change was unsuccessful
    """

    def change_blank(self, blank):
        if blank is not None:
            self.G.blank = blank
        return blank

    """
    Changes the left end marker of the ATM
    :param left_end the new left end marker
    :returns None iff the change was unsuccessful
    """

    def change_left_end(self, left_end):
        if left_end is not None:
            self.G.left_end = left_end
        return left_end

    """
    Changes the start state of the ATM
    :param the new start state
    :returns the new start state if the change is successful else None
    """

    def change_start(self, start):
        if self.G.is_vertex(start):
            self.G.start = start
            return start
        return None

    """
    Adds a symbol to Sigma
    :param a the symbol to add
    """

    def add_input_symbol(self, a):
        self.G.Sigma |= {a}

    """
    Removes a symbol from Sigma
    :param a the symbol to be removed
    :returns a if successful and None otherwise
    """

    def remove_input_symbol(self, a):
        if a in self.G.Sigma:
            self.G.Sigma.remove(a)
            return a
        return None


    """
    Adds a state to the ATM with its type
    :param qty the new state concatenated with ',' concatenated with the type
    :returns q if adding the state was successful and None otherwise
    """

    def add_state(self, qty):
        q, ty = qty.rsplit(',', 1)
        if self.G.is_vertex(q) or (ty != '∨' and ty != '∧'):
            return None
        self.G.add_vertex(q)
        self.t[q] = ty
        self.G.t = lambda x: self.t[x]
        return q

    """
    Removes a state from the ATM
    :param q the state to be removed
    :returns q if the state was removed successfully and None otherwise
    """

    def remove_state(self, q):
        if self.G.is_vertex(q):
            self.G.remove_vertex(q)
            del self.t[q]
            return q
        return None

    """
    Adds a transition to the ATM
    :param p the current state
    :param q the next state
    :param abd string of form '(the symbol read)->(the symbol to write on the tape),('L' or 'R')'
    :returns p if the transition was added successfully and None otherwise
    """

    def add_transition(self, p, q, abd):
        if self.G.is_vertex(p) and self.G.is_vertex(q):
            a, bd = abd.split("->", 1)
            b, d = bd.rsplit(',', 1)
            if d == 'L' or d == 'R':
                self.G.add_edge(p, q, (a, b, d))
                return p
        return None

    """
    Removes a transition from the ATM
    :param p the current state
    :param q the next state
    :param abd string of form '(the symbol read)->(the symbol to write on the tape),('L' or 'R')'
    :returns p if the transition was removed successfully and None otherwise
    """

    def remove_transition(self, p, q, abd):
        a, bd = abd.split("->", 1)
        b, d = bd.rsplit(',', 1)
        if self.G.is_weight(p, q, (a, b, d)):
            self.G.remove_edge(p, q, (a, b, d))
            return p
        return None

