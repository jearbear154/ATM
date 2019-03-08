import unittest
from simulator.tree import Tree

"""
Tests the functionality of the Tree class
"""


class TreeTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = Tree("root", [Tree("left"), Tree("right")])
        self.tree2 = Tree("root", [Tree("left"), Tree("right")])
        self.tree3 = Tree("root", [Tree("lef"), Tree("righ")])
        self.tree4 = Tree("root")
        self.tree6 = Tree(None, [Tree("left"), Tree("right")])
        self.tree7 = Tree("root", [Tree("left", [Tree("leftleft")]), Tree("right")])

    def test_equality(self):
        self.assertEqual(self.tree1, self.tree2)
        self.assertEqual(self.tree2, self.tree1)
        self.assertNotEqual(self.tree1, self.tree3)
        self.assertNotEqual(self.tree2, self.tree3)
        self.assertNotEqual(self.tree3, self.tree1)
        self.assertNotEqual(self.tree3, self.tree2)

        self.assertNotEqual(self.tree1, self.tree4)
        self.assertNotEqual(self.tree1, self.tree6)

    def test_depth(self):
        self.assertEqual(1, self.tree1.depth())
        self.assertEqual(0, self.tree4.depth())
        self.assertEqual(2, self.tree7.depth())


if __name__ == '__main__':
    unittest.main()
