from graph import Graph
from helpers import compute_distance


class TSPManager(object):
    def __init__(self, songs):
        
        self.songs = songs

        self.graph = None

    def perform(self):
        """
        Computes the graph and performs TSP resolution on it
        """

        self.compute_graph()
        self.perform_tsp()

    def compute_graph(self):
        self.graph = Graph(self.songs)
        for start_index, start_node in enumerate(self.nodes):
            for end_index, end_node in enumerate(self.nodes):
                if start_index != end_index:
                    dist = compute_distance(start_node, end_node)
                    self.graph.add_edge(start_index, end_index, dist)
    
    def perform_tsp(self):
        pass
