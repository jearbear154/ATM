import unittest
from simulator.computation_tree import ComputationTree
from simulator.atm import ATM
from simulator.tree import Tree

"""
Tests the functionality of the ComputationTree class
"""


class TestComputationTree(unittest.TestCase):
    def setUp(self):
        self.tree1 = ComputationTree(ATM.Configuration('q', 2, ['|-', '0', '1']),
                                     [ComputationTree(ATM.Configuration('q2', 1, ['|-', '2', '0', '1', '0', '1']),
                                                      [ComputationTree(ATM.Configuration('q3', 0, ['|-', '0']))])])

    def test_proof_tree(self):
        proof_tree = Tree(('q', '1'), [Tree(('q2', '2'), [Tree(('q3', '|-'))])])
        self.assertEqual(proof_tree, self.tree1.proof_tree())

    def test_time(self):
        self.assertEqual(2, self.tree1.time())

    def test_space(self):
        self.assertEqual(5, self.tree1.space())


if __name__ == '__main__':
    unittest.main()
