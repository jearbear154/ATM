import unittest
from networkx.drawing.nx_pydot import to_pydot
from converter.atm_graph import ATMGraph
from model.model import Model

"""
Tests the functionality of the Model class
"""


class ModelFunctionality(unittest.TestCase):
    def setUp(self):
        self.M = Model()
        Q = {'q1,∨', 'q2,∨', 'q3,∨', 'q4,∨', 'q5,∨', 'qaccept,∧'}
        for q in Q:
            self.M.add_state(q)
        Sig = {'0'}
        for a in Sig:
            self.M.add_input_symbol(a)
        self.M.change_left_end('|-')
        self.M.change_blank(' ')
        self.M.change_start('q1')
        delta = {('q1', 'q1'): {'|-->|-,R'},
                 ('q1', 'q2'): {'0-> ,R'},
                 ('q2', 'qaccept'): {' -> ,R'},
                 ('q2', 'q2'): {'x->x,R'},
                 ('q2', 'q3'): {'0->x,R'},
                 ('q3', 'q4'): {'0->0,R'},
                 ('q3', 'q3'): {'x->x,R'},
                 ('q3', 'q5'): {' -> ,L'},
                 ('q4', 'q4'): {'x->x,R'},
                 ('q4', 'q3'): {'0->x,R'},
                 ('q5', 'q5'): {'x->x,L', '0->0,L'},
                 ('q5', 'q2'): {' -> ,R'}}
        for p, q in delta:
            for m in delta[(p, q)]:
                self.M.add_transition(p, q, m)

        self.G = ATMGraph({'0'}, '|-', ' ', 'q1',
                          lambda q: '∧' if q == 'qaccept' else '∨')
        for i in range(1, 6):
            self.G.add_vertex('q' + str(i))
        self.G.add_vertex('qaccept')
        self.G.add_edge('q1', 'q1', ('|-', '|-', 'R'))
        self.G.add_edge('q1', 'q2', ('0', ' ', 'R'))
        self.G.add_edge('q2', 'qaccept', (' ', ' ', 'R'))
        self.G.add_edge('q2', 'q2', ('x', 'x', 'R'))
        self.G.add_edge('q2', 'q3', ('0', 'x', 'R'))
        self.G.add_edge('q3', 'q4', ('0', '0', 'R'))
        self.G.add_edge('q3', 'q3', ('x', 'x', 'R'))
        self.G.add_edge('q3', 'q5', (' ', ' ', 'L'))
        self.G.add_edge('q4', 'q4', ('x', 'x', 'R'))
        self.G.add_edge('q4', 'q3', ('0', 'x', 'R'))
        self.G.add_edge('q5', 'q5', ('x', 'x', 'L'))
        self.G.add_edge('q5', 'q5', ('0', '0', 'L'))
        self.G.add_edge('q5', 'q2', (' ', ' ', 'R'))

    def test_additions(self):
        assert self.G == self.M.G
        assert self.M.add_transition("r", "f", "j") is None
        assert self.M.add_state("q,r") is None
        assert self.M.change_start("reject") is None

    def test_graphical_representation(self):
        H = self.M.graphical_representation()
        F = to_pydot(H)
        F.write_png('graph1.png', prog='dot')

    def test_simulation(self):
        t, s, T = self.M.simulate(['0', '0', '0', '0'])
        assert t == 22 and s == 6
        F = to_pydot(T)
        F.write_png('tree.png', prog='dot')
        assert self.M.simulate(['0', '0', '0']) is None
        assert self.M.simulate(['0', '0', '0', '0'], 10, 6) is None
        assert self.M.simulate(['0', '0', '0', '0'], 22, 4) is None


class ModelRemovalTest(unittest.TestCase):
    def setUp(self):
        self.M = Model()
        Q = {'q1,∨', 'q2,∨', 'q3,∨', 'q4,∨', 'q5,∨', 'qaccept,∧'}
        for q in Q:
            self.M.add_state(q)
        Sig = {'0'}
        for a in Sig:
            self.M.add_input_symbol(a)
        self.M.change_left_end('|-')
        self.M.change_blank(' ')
        self.M.change_start('q1')
        delta = {('q1', 'q1'): {'|-->|-,R'},
                 ('q1', 'q2'): {'0-> ,R'},
                 ('q2', 'qaccept'): {' -> ,R'},
                 ('q2', 'q2'): {'x->x,R'},
                 ('q2', 'q3'): {'0->x,R'},
                 ('q3', 'q4'): {'0->0,R'},
                 ('q3', 'q3'): {'x->x,R'},
                 ('q3', 'q5'): {' -> ,L'},
                 ('q4', 'q4'): {'x->x,R'},
                 ('q4', 'q3'): {'0->x,R'},
                 ('q5', 'q5'): {'x->x,L', '0->0,L'},
                 ('q5', 'q2'): {' -> ,R'}}
        for p, q in delta:
            for m in delta[(p, q)]:
                self.M.add_transition(p, q, m)

    def test_removals(self):
        assert self.M.remove_state("r") is None
        assert self.M.remove_transition("f", "t", "l->5,8") is None
        assert self.M.remove_state('q5') == 'q5'
        assert not self.M.G.is_vertex('q5')
        assert self.M.remove_transition('q4', 'q4', 'x->x,R') == 'q4'
        assert self.M.remove_input_symbol("b") is None
        assert self.M.remove_input_symbol('0') == '0'


if __name__ == '__main__':
    unittest.main()
