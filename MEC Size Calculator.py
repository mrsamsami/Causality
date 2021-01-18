import networkx as nx
import math


class Graph(object):
    def __init__(self, graph=None, edges=None):
        """
        The graph class that utilizes the networkx object for graph operations.
        :param graph: A networkx graph to initialize the graph.
        :param edges: A list of edges to initialize the graph.
        """
        super(Graph, self).__init__()

        if graph is None:
            # We use digraph so that we can create a partial directed graph
            self.graph = nx.DiGraph()
            if edges is not None:
                self.add_edges(edges)

        else:
            self.graph = graph.copy()

    def nodes(self):
        return list(self.graph.nodes)

    def edges(self):
        edges = []
        for e in self.graph.edges:
            edges.append(e + (self.graph[e[0]][e[1]]['dir'],))
        return edges

    def add_edges(self, edges):
        """
        Each edge uv has a `dir` property that determines its direction:
            * -1: u <- v
            * +1: u -> v
            * 0:  u -- v
        """
        edges = [e + ({'dir': 0},) for e in edges]
        self.graph.add_edges_from(edges)

    def remove_edge(self, u, v):
        self.graph.remove_edge(u, v)

    def has_edge(self, U, V):
        # Check if there is any edge between a single (or set of) node U and a single (or set of) node V
        if not isinstance(U, list):
            U = list(U)
        if not isinstance(V, list):
            V = list(V)

        for u in U:
            for v in V:
                if self.graph.has_edge(u, v):
                    return True
        return False

    def orient(self, U, V):
        # Orient edges from a single (or set of) node U to a single (or set of) node V
        if not isinstance(U, list):
            U = list(U)
        if not isinstance(V, list):
            V = list(V)

        for u in U:
            for v in V:
                if self.has_edge(u, v):
                    self.graph[u][v]['dir'] = 1
                    self.graph[v][u]['dir'] = -1

    def neighbors(self, v):
        edges = []
        for u in self.graph.neighbors(v):
            edges.append((u, self.graph[v][u]['dir']))
        return edges

    def dir(self, v, u):
        return self.graph[v][u]['dir']

    def subgraph(self, nodes):
        return Graph(self.graph.subgraph(nodes))

    def components(self):
        return nx.weakly_connected_components(self.graph)

    def copy(self):
        return Graph(self.graph)


def chain_com(graph, v):
    A = [v]
    B = graph.nodes()
    B.remove(v)
    O = []

    while B:
        T = [w for w in B if graph.has_edge(w, A)]
        graph.orient(A, T)

        while True:
            no_orientation = True

            for y in T:
                for z in T:
                    if y == z or not graph.has_edge(y, z) or graph.dir(y, z) != 0:
                        continue

                    edges = graph.neighbors(y)
                    for x, d in edges:
                        if x != z and not graph.has_edge(x, z) and d == -1:
                            graph.orient(y, z)
                            no_orientation = False
                            break

            if no_orientation:
                break

        A = list(T)
        for v in T:
            B.remove(v)

        subgraph = graph.subgraph(T)
        for u, v, d in subgraph.edges():
            if d != 0:
                subgraph.remove_edge(u, v)

        for c in subgraph.components():
            O.append(subgraph.subgraph(c))

    return O


def size_MEC(graph):
    n = len(graph.edges()) / 2
    p = len(graph.nodes())

    if n == p - 1:
        return p
    if n == p:
        return 2 * p
    if n == p * (p - 1) / 2 - 2:
        return (p ** 2 - p - 4) * math.factorial(p - 3)
    if n == p * (p - 1) / 2 - 1:
        return 2 * math.factorial(p - 1) - math.factorial(p - 2)
    if n == p * (p - 1) / 2:
        return math.factorial(p)

    total_size = 0
    for v in graph.nodes():
        components = chain_com(graph.copy(), v)
        size = 1
        for c in components:
            size *= size_MEC(c)
        total_size += size

    return total_size


"""
Input format:
    First line: Number of edges
    The i'th line (2 <= i <= Number of edges + 1): u v
"""

edges = []
inp = input()
while inp and not inp.isspace():
    u, v = inp.split()
    edges.append((u, v))
    edges.append((v, u))
    inp = input()

print(size_MEC(Graph(edges = edges)))
