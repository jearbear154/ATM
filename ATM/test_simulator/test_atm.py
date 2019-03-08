import unittest
from simulator.atm import ATM

"""
Tests the functionality of the ATM class
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
            if q == 'qaccept':
                return '∧'
            else:
                return '∨'

        self.M = ATM(Q, Sigma, Gamma, '|-', ' ', delta, 'q1', t)

    def test_init(self):
        assert self.M.machine_valid()

    def test_equality(self):
        assert self.M == ATM(self.M.Q, self.M.Sigma, self.M.Gamma, self.M.left_end, self.M.blank,
                             self.M.delta, self.M.start, self.M.t)
        assert self.M != ATM(self.M.Q, self.M.Sigma, self.M.Gamma, self.M.left_end, self.M.blank,
                             lambda q, a: {}, self.M.start, self.M.t)
        assert self.M != ATM(self.M.Q, self.M.Sigma, self.M.Gamma, self.M.left_end, self.M.blank,
                             self.M.delta, self.M.start, lambda q: '∧')


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
        self.N.Configuration(None, None, None)

    def test_init(self):
        assert self.N.machine_valid()

    def test_equality(self):
        assert self.N != ATM({'q1', 'q2', 'q3', 'q4', 'qaccept', 'qreject'}, self.N.Sigma,
                             self.N.Gamma, '|-', ' ', self.N.delta, 'q1', self.N.t)


class InvalidATMTest(unittest.TestCase):
    def setUp(self):
        self.invalid_states = ATM({'q0', 'q1'}, None, None, None, None, None, 'q2', None)
        self.invalid_alphabets1 = ATM({'q0', 'q1'}, {'a', 'b', 'c'}, {'a', 'b', '|-', ' '}, '|-', ' ', None, 'q0', None)
        self.invalid_alphabets2 = ATM({'q0', 'q1'}, {'a', 'b'}, {'a', 'b', '|-', ' '}, '|', ' ', None, 'q0', None)
        self.invalid_alphabets3 = ATM({'q0', 'q1'}, {'a', 'b', '|-'}, {'a', 'b', '|-', ' '}, '|-', ' ', None, 'q0', None)
        self.invalid_left_transition = ATM({'q1','q2'}, {'a'}, {'a', '|-', ' '}, '|-', ' ',
                                            lambda q, a: {(q, a, 'L')}, None, lambda q: '∨')
        self.no_halting_state = ATM({'q1'}, {'a'}, {'a', '|-', ' '}, '|-', ' ',
                                           lambda q, a: {(q, a, 'R')}, None, lambda q: '∨')
        self.invalid_type_function = ATM({'q1', 'q2'}, None, None, None, None, None, None, lambda q: ' ')

    def test_states_correct(self):
        assert not self.invalid_states.states_correct()

    def test_alphabets_consistent(self):
        assert not self.invalid_alphabets1.alphabets_consistent()
        assert not self.invalid_alphabets2.alphabets_consistent()
        assert not self.invalid_alphabets3.alphabets_consistent()

    def test_transition_function_valid(self):
        self.invalid_left_transition.delta = lambda q, a: [(q, a, 'L')]
        self.no_halting_state.delta = lambda q, a: [(q, a, 'R')]
        assert not self.invalid_left_transition.transition_function_valid()
        assert not self.no_halting_state.transition_function_valid()

    def test_type_function_valid(self):
        self.invalid_type_function.t = lambda q: ' '
        assert not self.invalid_type_function.type_function_valid()


if __name__ == '__main__':
    unittest.main()
