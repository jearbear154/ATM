import unittest
from converter.multigraph import MultiGraph

"""
Tests the functionality of the MultiGraph class
"""


class MultiGraphTest(unittest.TestCase):
    def test_add_vertex(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        assert G.is_vertex("u")
        assert G.is_vertex("v")

    def test_remove_vertex(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_edge("v", "u", 4)
        assert G.is_vertex("u")
        assert G.is_vertex("v")
        assert G.is_edge("v", "u")
        G.remove_vertex("u")
        assert not G.is_vertex("u")
        assert not G.is_edge("v", "u")

    def test_add_edge(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_edge("u", "v", 5)
        G.add_edge("u", "v", 8)
        self.assertEqual({5, 8}, set(G.weights("u", "v")))
        self.assertEqual({("u", "v")}, set(G.edges()))

    def test_remove_edge(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_edge("u", "v", 5)
        G.add_edge("u", "v", 8)
        self.assertEqual({5, 8}, set(G.weights("u", "v")))
        self.assertEqual({("u", "v")}, set(G.edges()))
        G.remove_edge("u", "v", 5)
        self.assertEqual({8}, set(G.weights("u", "v")))
        assert not G.is_weight("u", "v", 5)

    def test_is_vertex(self):
        G = MultiGraph()
        G.add_vertex("u")
        assert G.is_vertex("u")

    def test_is_edge(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_edge("u", "v", 5)
        G.add_edge("u", "v", 8)
        assert G.is_edge("u", "v")
        assert not G.is_edge("v", "u")
        assert not G.is_edge("h", "v")

    def test_is_weight(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_edge("u", "v", 5)
        G.add_edge("u", "v", 8)
        assert G.is_weight("u", "v", 5)
        assert G.is_weight("u", "v", 8)
        assert not G.is_weight("u", "v", 3)
        assert not G.is_weight("v", "u", 4)

    def test_vertices(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_vertex("w")
        self.assertEqual({"u", "v", "w"}, set(G.vertices()))

    def test_edges(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_vertex("w")
        G.add_edge("u", "v", 0)
        G.add_edge("u", "w", 0)
        G.add_edge("v", "w", 0)
        self.assertEqual({("u", "v"), ("u", "w"), ("v", "w")}, set(G.edges()))

    def test_weights(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_vertex("w")
        G.add_edge("u", "w", 3)
        G.add_edge("u", "w", 4)
        G.add_edge("v", "w", 9)
        self.assertEqual({3, 4}, set(G.weights("u", "w")))
        self.assertEqual({9}, set(G.weights("v", "w")))
        assert G.weights("h", "t") is None

    def test_equality(self):
        G = MultiGraph()
        G.add_vertex("u")
        G.add_vertex("v")
        G.add_vertex("w")
        G.add_edge("u", "w", 3)
        G.add_edge("u", "w", 4)
        G.add_edge("v", "w", 9)
        H = MultiGraph()
        H.add_vertex("u")
        H.add_vertex("v")
        H.add_vertex("w")
        H.add_edge("u", "w", 3)
        H.add_edge("u", "w", 4)
        H.add_edge("v", "w", 9)
        assert G == H
        H.adjList["u"] = dict()
        assert G != H
        H = MultiGraph()
        assert G != H
        H = MultiGraph()
        H.add_vertex("u")
        H.add_vertex("v")
        H.add_vertex("w")
        H.add_edge("u", "w", 3)
        H.add_edge("u", "w", 5)
        H.add_edge("v", "w", 9)
        assert G != H


if __name__ == '__main__':
    unittest.main()
