import unittest
from converter.atm_graph import ATMGraph
from simulator.atm import ATM
from converter.atm_converter import ATMConverter

"""
Tests the functionality of the ATMConverter class
"""


class ATMConverterDeterministicTest(unittest.TestCase):
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

        Q = {'q1', 'q2', 'q3', 'q4', 'q5', 'qaccept'}
        Sigma = {'0'}
        Gamma = {' ', 'x', '0', '|-'}

        def delta(q, a):
            transitions = {('q1', '|-'): {('q1', '|-', 'R')}, ('q1', '0'): {('q2', ' ', 'R')},
                ('q2', ' '): {('qaccept', ' ', 'R')}, ('q2', 'x'): {('q2', 'x', 'R')}, ('q2', '0'): {('q3', 'x', 'R')},
                ('q3', '0'): {('q4', '0', 'R')}, ('q3', 'x'): {('q3', 'x', 'R')}, ('q3', ' '): {('q5', ' ', 'L')},
                ('q4', 'x'): {('q4', 'x', 'R')}, ('q4', '0'): {('q3', 'x', 'R')}, ('q5', 'x'): {('q5', 'x', 'L')},
                ('q5', '0'): {('q5', '0', 'L')}, ('q5', ' '): {('q2', ' ', 'R')}}
            return set() if (q, a) not in transitions else transitions[(q, a)]

        def t(q):
            if q == 'qaccept':
                return '∧'
            else:
                return '∨'

        self.M = ATM(Q, Sigma, Gamma, '|-', ' ', delta, 'q1', t)

    def test_atm_to_graph(self):
        assert self.G == ATMConverter.to_graph(self.M)

    def test_graph_to_atm(self):
        assert self.M == ATMConverter.from_graph(self.G)


class ATMConverterNonDeterministicTest(unittest.TestCase):
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

        def delta(q, a):
            transitions = {('q1', '|-'): {('q1', '|-', 'R')}, ('q1', '0'): {('q1', '0', 'R')},
                           ('q1', '1'): {('q1', '1', 'R'), ('q2', '1', 'R')},
                           ('q2', '0'): {('q3', '0', 'R')}, ('q2', '1'): {('q3', '1', 'R')},
                           ('q3', '0'): {('q4', '0', 'R')}, ('q3', '1'): {('q4', '1', 'R')},
                           ('q4', ' '): {('qaccept', ' ', 'R')}}
            return set() if (q, a) not in transitions else transitions[(q, a)]

        def t(q):
            if q == 'qaccept':
                return '∧'
            else:
                return '∨'

        self.N = ATM({'q1', 'q2', 'q3', 'q4', 'qaccept'}, {'0', '1'}, {'0', '1', '|-', ' '}, '|-', ' ', delta, 'q1', t)

    def test_atm_to_graph(self):
        assert self.H == ATMConverter.to_graph(self.N)

    def test_graph_to_atm(self):
        assert self.N == ATMConverter.from_graph(self.H)


class ATMConverterDifferentTest(unittest.TestCase):
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
        self.H.add_edge('q4', 'qaccept', (' ', ' ', 'R'))

        def delta(q, a):
            transitions = {('q1', '|-'): [('q1', '|-', 'R')], ('q1', '0'): [('q1', '0', 'R')],
                           ('q1', '1'): [('q1', '1', 'R'), ('q2', '1', 'R')],
                           ('q2', '0'): [('q3', '0', 'R')], ('q2', '1'): [('q3', '1', 'R')],
                           ('q3', '0'): [('q4', '0', 'R')], ('q3', '1'): [('q4', '1', 'R')],
                           ('q4', ' '): [('qaccept', ' ', 'R')]}
            return [] if (q, a) not in transitions else transitions[(q, a)]

        def t(q):
            if q == 'qaccept':
                return '∧'
            else:
                return '∨'

        self.N = ATM({'q1', 'q2', 'q3', 'q4', 'qaccept'}, {'0', '1'}, {'0', '1', '|-', ' '}, '|-', ' ', delta, 'q1', t)

    def test_atm_to_graph(self):
        assert self.H != ATMConverter.to_graph(self.N)

    def test_graph_to_atm(self):
        assert self.N != ATMConverter.from_graph(self.H)


if __name__ == '__main__':
    unittest.main()
