import sys
import heapq
import networkx


class DijkstraSolver:
    def __init__(self, number_of_nodes, graph, graphType):
        self.number_of_nodes = number_of_nodes
        self.graph = graph
        self.path = [-1] * (number_of_nodes + 5)
        self.pathDistance = [0] * (number_of_nodes + 5)
        self.nxGraph = networkx.Graph() if graphType == "Undirected" else networkx.DiGraph()

    def solve(self, source, destination_Val):
        min_distance = [sys.maxsize] * (self.number_of_nodes + 5)
        min_distance[source] = 0
        priority_queue = [(0, source)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > min_distance[current_node]:
                continue

            for i in range(len(self.graph.adjacency_list[current_node])):
                weight = self.graph.adjacency_list[current_node][i].weight
                to = self.graph.adjacency_list[current_node][i].to
                distance = current_distance + weight
                if distance < min_distance[to]:
                    self.path[to] = current_node
                    self.pathDistance[to] = weight
                    min_distance[to] = distance
                    heapq.heappush(priority_queue, (distance, to))
        self.getPath(destination_Val, [])
        return self.nxGraph

    def getPath(self, current_node, path):
        if self.path[current_node] == -1:
            return
        self.nxGraph.add_edge(str(self.path[current_node]), str(current_node), weight=self.pathDistance[current_node])
        self.getPath(current_node=self.path[current_node], path=path)
