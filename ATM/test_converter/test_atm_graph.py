import unittest
from converter.atm_graph import ATMGraph

"""
Tests the functionality of the ATMGraph
"""


class ATMGraphDeterministicTest(unittest.TestCase):
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

    def test_vertices(self):
        for i in range(1, 6):
            assert self.G.is_vertex('q' + str(i))
        assert self.G.is_vertex('qaccept')

    def test_edges(self):
        self.assertEqual({('x', 'x', 'L'), ('0', '0', 'L')}, set(self.G.weights('q5', 'q5')))
        self.assertEqual({('0', ' ', 'R')}, set(self.G.weights('q1', 'q2')))

    def test_explicit_attributes(self):
        self.assertEqual({'0'}, self.G.Sigma)
        self.assertEqual('|-', self.G.left_end)
        self.assertEqual(' ', self.G.blank)
        self.assertEqual('q1', self.G.start)
        for q in self.G.vertices():
            if q == 'qaccept':
                self.assertEqual('∧', self.G.t(q))
            else:
                self.assertEqual('∨', self.G.t(q))

    def test_equality(self):
        assert self.G == self.G


class ATMGraphNonDeterministicTest(unittest.TestCase):
    def setUp(self):
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

    def test_vertices(self):
        self.assertEqual({'q1', 'q2', 'q3', 'q4', 'qaccept'}, set(self.H.vertices()))

    def test_edges(self):
        self.assertEqual({('q1', 'q1'), ('q1', 'q2'), ('q2', 'q3'), ('q3', 'q4'), ('q4', 'qaccept')}, set(self.H.edges()))
        self.assertEqual({('|-', '|-', 'R'), ('0', '0', 'R'), ('1', '1', 'R')}, set(self.H.weights('q1', 'q1')))
        self.assertEqual({('0', '0', 'R'), ('1', '1', 'R')}, set(self.H.weights('q3', 'q4')))

    def test_explicit_attributes(self):
        self.assertEqual({'0', '1'}, self.H.Sigma)
        self.assertEqual('|-', self.H.left_end)
        self.assertEqual(' ', self.H.blank)
        self.assertEqual('q1', self.H.start)
        for q in self.H.vertices():
            if q == 'qaccept':
                self.assertEqual('∧', self.H.t(q))
            else:
                self.assertEqual('∨', self.H.t(q))


if __name__ == '__main__':
    unittest.main()
