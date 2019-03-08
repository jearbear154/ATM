import unittest
from simulator.atm import ATM
from simulator.atm_simulator import ATMSimulator
from graphics.tree_converter import TreeConverter
from networkx.drawing.nx_pydot import to_pydot
from networkx.classes.graph import Graph

"""
Tests the functionality of the TreeConverter class
"""


class TestTreeConverter(unittest.TestCase):
    def setUp(self):
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
            if q == 'qaccept' or q == 'q1':
                return '∧'
            else:
                return '∨'

        self.M = ATM(Q, Sigma, Gamma, '|-', ' ', delta, 'q1', t)

    def test_to_graphics(self):
        T = TreeConverter.to_graphics(ATMSimulator.simulate(self.M, ['0', '0', '0', '0']))
        H = to_pydot(T)
        H.write_png('tree.png', prog='dot')

    def test_to_nx_graph(self):
        T = ATMSimulator.simulate(self.M, ['0']).proof_tree()
        H = Graph()
        j = TreeConverter.to_nx_graph(T, H, 1)
        assert j == 5
        for i in range(1, 5):
            assert H.has_node(i)
        assert not H.has_node(5)



if __name__ == '__main__':
    unittest.main()
