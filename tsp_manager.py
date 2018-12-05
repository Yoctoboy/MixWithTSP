from __future__ import print_function

from copy import deepcopy
import cplex
import sys

from distance_computer import DistanceComputer
from graph import Graph
from helpers import get_shifted_key_tone, tone_repr
from tsp_solver import TSPSolver


class TSPManager(object):
    def __init__(self, songs, shifts_allowed, result_file):
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
        self.result_file = result_file

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

    def precompute_nodes(self):
        """
        Precomputes nodes (in case of key-shifting being allowed)
        """

        self.nodes = [0]
        current_index = 1
        for song in self.songs:
            for shift in range(-self.shifts_allowed, self.shifts_allowed + 1):
                current_song = deepcopy(song)
                current_song["shifted_key_tone"] = get_shifted_key_tone(song["key_tone"], shift)
                current_song["index"] = current_index
                current_song["shift"] = shift
                self.nodes.append(current_song)
                current_index += 1
    
    def perform_tsp(self):
        """
        Calls a TSPSolver object to solve the tsp on the instance
        
        Returns:
            list, int -- optimal path, and its value
        """

        solver =  TSPSolver(self.nodes, self.graph, 2 * self.shifts_allowed + 1)
        solver.create_model()
        return solver.solve()

    def print_results(self, path, value):
        file = open(self.result_file, 'a+') if self.result_file else sys.stdout
        print ("\nBEST PATH FOUND (value={}):\n".format(value), file=file)
        print ("                 Track name                   |  BPM   | Tone | Shifted Tone | Key Shift", file=file)
        print ("----------------------------------------------------------------------------------------", file=file)
        for node in path:
            song = self.nodes[node]
            print("{:<45} | {:6.2f} |  {:<3} |      {:<3}     |    {:>2}".format(song["name"], round(song["bpm"], 2), tone_repr(song["key_tone"]), tone_repr(song["shifted_key_tone"]), song["shift"]), file=file)
        print("")