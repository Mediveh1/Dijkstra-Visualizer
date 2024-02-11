class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge_undirected(self, vertex1, vertex2, weight):
        self.adjacency_list[vertex1].append(Edge(vertex2, weight))
        self.adjacency_list[vertex2].append(Edge(vertex1, weight))  # Assuming an undirected graph

    def add_edge_directed(self, vertex1, vertex2, weight):
        self.adjacency_list[vertex1].append(Edge(vertex2, weight))

class Edge:
    def __init__(self, to_val, weight):
        self.to = to_val
        self.weight = weight
