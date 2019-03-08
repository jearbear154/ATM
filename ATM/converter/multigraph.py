
"""
MultiGraph --- class that represents a general dynamic directed multi-graph
:author Jeremy McMahan
"""


class MultiGraph:
    """
    Construct the empty graph
    """

    def __init__(self):
        self.adjList = dict()

    """
    Adds a vertex to the graph
    :param u the vertex to be added
    """

    def add_vertex(self, u):
        self.adjList[u] = dict()

    """
    Removes a vertex from the graph if it exists
    """

    def remove_vertex(self, u):
        if self.is_vertex(u):
            del self.adjList[u]
            for w in self.vertices():
                if u in self.adjList[w]:
                    del self.adjList[w][u]

    """
    Adds an edge with weight w to the graph
    :param u the tail of the edge
    :param v the head of the edge
    :param w the weight of the edge
    """

    def add_edge(self, u, v, w):
        if v not in self.adjList[u]:
            self.adjList[u][v] = set()
        self.adjList[u][v] |= {w}

    """
    Removes a multi-edge from the graph if it exists
    :param u the tail of the edge
    :param v the head of the edge
    :param w the weight of the edge
    """

    def remove_edge(self, u, v, w):
        if self.is_weight(u, v, w):
            self.adjList[u][v].remove(w)

    """
    Determines if a vertex is in the graph
    :param u the vertex
    :returns True iff u is a vertex of the graph
    """

    def is_vertex(self, u):
        return u in self.adjList

    """
    Determines if a directed multi-edge exists
    :param u the tail of the edge
    :param v the head of the edge
    :returns True iff the edge u->v exists
    """

    def is_edge(self, u, v):
        if self.is_vertex(u) and self.is_vertex(v):
            return v in self.adjList[u]
        return False

    """
    Determines if a directed multi-edge exists with a specified weight
    :param u the tail of the edge
    :param v the head of the edge
    :param w the weight of the edge
    :returns True iff there is an edge u->v in the graph with weight w
    """

    def is_weight(self, u, v, w):
        if self.is_edge(u, v):
            return w in self.weights(u, v)
        return False

    """
    :returns a list of the vertices of the graph
    """

    def vertices(self):
        return set(self.adjList.keys())

    """
    :returns a set of the edges of the graph
    """

    def edges(self):
        edges = set()
        for u in self.vertices():
            for v in self.adjList[u].keys():
                edges |= {(u, v)}
        return edges

    """
    Returns a list of weights associated to the multi-edge u -> v
    :param u the tail of the edge
    :param v the head of the edge
    :returns the weights on each edge u->v if any exist, else None
    """

    def weights(self, u, v):
        if self.is_edge(u, v):
            return self.adjList[u][v]
        return None

    """
    Determines if two multi-graphs are equal
    :param other the other multi-graph
    :returns True iff the two multi-graphs are equal
    """

    def __eq__(self, other):
        if self.vertices() != other.vertices():
            return False
        elif self.edges() != other.edges():
            return False
        else:
            for u, v in self.edges():
                if self.weights(u, v) != other.weights(u, v):
                    return False
            return True

    """
    Determines if two multi-graphs are not equal
    :param other the other multi-graph
    :returns True iff the two multi-graphs are not equal
    """

    def __ne__(self, other):
        return not (self == other)
