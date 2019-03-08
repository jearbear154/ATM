import unittest
from converter.atm_graph import ATMGraph
from graphics.graph_converter import GraphConverter
from networkx.drawing.nx_pydot import to_pydot

"""
Tests the functionality of the GraphConverter class
"""


class TestGraphConverter(unittest.TestCase):
    def setUp(self):
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

        self.H = ATMGraph({'0', '1'}, '|-', ' ', 'q1', lambda q: '∧' if q == 'qaccept' else '∨')
        for i in range(1, 5):
            self.H.add_vertex('q' + str(i))
        self.H.add_vertex('qaccept')
        self.H.add_edge('q1', 'q1', ('|-', '|-', 'R'))
        self.H.add_edge('q1', 'q1', ('0', '0', 'R'))
        self.H.add_edge('q1', 'q1', ('1', '1', 'R'))
        self.H.add_edge('q1', 'q2', ('1', '1', 'R'))
        self.H.add_edge('q2', 'q3', ('0', '0', 'R'))
        self.H.add_edge('q2', 'q3', ('1', '1', 'R'))
        self.H.add_edge('q3', 'q4', ('0', '0', 'R'))
        self.H.add_edge('q3', 'q4', ('1', '1', 'R'))
        self.H.add_edge('q4', 'qaccept', (' ', ' ', 'R'))

    def test_to_graphics(self):
        H = GraphConverter.to_graphics(self.G)
        F = to_pydot(H)
        F.write_png('graph1.png', prog='dot')
        H = GraphConverter.to_graphics(self.H)
        F = to_pydot(H)
        F.write_png('graph2.png', prog='dot')

    def test_from_graphics(self):
        states_and_types = {'q1,∨', 'q2,∨', 'q3,∨', 'q4,∨', 'q5,∨', 'qaccept,∧'}
        Sigma = {'0'}
        left_end = '|-'
        blank = ' '
        start = 'q1'
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
        H = GraphConverter.from_graphics(states_and_types, Sigma, left_end, blank, start, delta)
        assert H == self.G


if __name__ == '__main__':
    unittest.main()
