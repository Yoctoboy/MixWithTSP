from copy import deepcopy
import cplex

from distance_computer import DistanceComputer
from graph import Graph
from helpers import get_shifted_key_tone
from tsp_solver import TSPSolver


class TSPManager(object):
    def __init__(self, songs, shifts_allowed):
        """
        Constructor for the TSPManager
        
        Arguments:
            object {[type]} -- [description]
            songs {list} -- list of songs
            shifts_allowed {int} -- amount of key shifts allowed for the mix (recommended value : <=1)
        """
        
        self.songs = songs
        self.shifts_allowed = shifts_allowed
        self.solver = cplex.Cplex()

        # Filled during process
        self.nodes = []
        self.graph = None
        self.total_variables = 0

    def perform(self):
        """
        Computes the graph and performs TSP resolution on it
        """

        self.compute_graph()
        path, value = self.perform_tsp()
        self.print_results(path, value)

    def compute_graph(self):
        self.precompute_nodes()
        self.graph = Graph(self.nodes)
        for start_index, start_node in enumerate(self.nodes):
            for end_index, end_node in enumerate(self.nodes):
                if start_index != end_index:
                    dist = DistanceComputer(start_node, end_node).compute()
                    self.graph.add_edge(start_index, end_index, dist)
        print(self.graph)


    def precompute_nodes(self):
        """
        Precomputes nodes (in case of key-shifting being allowed)
        """

        for song in self.songs:
            for shift in range(-self.shifts_allowed, self.shifts_allowed + 1):
                current_song = deepcopy(song)
                current_song["key_tone"] = get_shifted_key_tone(song["key_tone"], shift)
                current_song["index"] = (2*self.shifts_allowed + 1) * (current_song["id"]) + (shift - self.shifts_allowed - 1)
                current_song["shift"] = shift
                print(current_song)
                self.nodes.append(current_song)
    
    def perform_tsp(self):

        solver =  TSPSolver(self.nodes, self.graph, 2 * self.shifts_allowed + 1)
        solver.create_model()
        return solver.solve()

    def print_results(self, path, value):
        print ("BEST PATH FOUND (value={}):".format(value))
        for edge in path:
            song = self.nodes[edge[0]]
            print(song["name"], song["bpm"], song["key_tone"], song["shift"])
        song = self.nodes[path[-1][1]]
        print(song["name"], song["bpm"], song["key_tone"], song["shift"])