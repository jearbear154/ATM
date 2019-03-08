import unittest
from simulator.atm import ATM
from simulator.atm_simulator import ATMSimulator

"""
Tests the functionality of the ATMSimulator class
"""


class TMTest(unittest.TestCase):
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

    def test_simulate(self):
        assert ATMSimulator.simulate(self.M, ['0', '0', '0', '0']) is not None
        assert ATMSimulator.simulate(self.M, ['0', '0', '0']) is None
        assert ATMSimulator.simulate(self.M, ['0', '0']) is not None
        assert ATMSimulator.simulate(self.M, ['0']) is not None
        assert ATMSimulator.simulate(self.M, ['0', '0', '0', '0', '0', '0']) is None
        assert ATMSimulator.simulate(self.M, ['0', '0', '0', '0', '0', '0', '0', '0']) is not None


class NTMTest(unittest.TestCase):
    def setUp(self):
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

    def test_simulate(self):
        assert ATMSimulator.simulate(self.N, ['0', '1', '0', '0']) is not None
        assert ATMSimulator.simulate(self.N, ['0', '0']) is None
        assert ATMSimulator.simulate(self.N, ['0', '0', '1', '1', '0', '0']) is not None
        assert ATMSimulator.simulate(self.N, ['a', 'c']) is None


if __name__ == '__main__':
    unittest.main()
