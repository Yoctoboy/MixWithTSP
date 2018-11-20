import cplex
import os
import sys


class TSPSolver(object):

    def __init__(self, nodes, graph, shifts_amount):
        """
        Constructor for TSPSolver
        
        Arguments:
            graph {Graph} -- Graph of all nodes, containning the matrix
            shifts_amount {int} -- amount of shifts per song
        """

        self.graph = graph
        self.graph_size = len(self.graph.nodes)
        self.shifts_amount = shifts_amount
        self.songs_amount = 1 + (self.graph_size - 1) / self.shifts_amount
        self.total_variables = self.graph_size * (self.graph_size + 1)
        self.solver = cplex.Cplex()

        for i in range(self.graph_size):
            self.graph.matrix[i][i] = 10000000
    
    def create_model(self):
        self.prepare_solver()
        self.add_constraints()
    
    def solve(self):
        #self.solver.write("mod.lp")
        self.solver.solve()
        return self.get_results(), int(self.solver.solution.get_objective_value())

    def prepare_solver(self):
        self.set_sense()
        self.set_variables()
        self.set_parameters()
    
    def set_sense(self):
        self.solver.objective.set_sense(self.solver.objective.sense.minimize)
    
    def set_variables(self):
        obj = self.get_obj()
        ub = self.get_ub()
        types = (self.graph_size ** 2) * [self.solver.variables.type.binary] + \
            self.graph_size * [self.solver.variables.type.integer]
        lb = [0 for _ in range(self.total_variables)]
        self.solver.variables.add(obj=obj, lb=lb, ub=ub, types=types)
        colnames = []
        oui = 0
        for start_song in range(self.songs_amount):
            for i in self.get_nodes_associated_to_song(start_song):
                for end_song in range(self.songs_amount):
                    for j in self.get_nodes_associated_to_song(end_song):
                        colnames.append("x_{}_{}__{}_{}".format(start_song, i % self.shifts_amount, end_song, j % self.shifts_amount))
                        oui +=1
        for i in range(self.graph_size):
            colnames.append("u_{}".format(i))
        self.solver.variables.set_names([(i, colnames[i]) for i in range(self.total_variables)])
    
    def set_parameters(self):
        #self.solver.parameters.mip.display.set(0)
        pass
    
    def get_obj(self):
        obj = [0 for _ in range(self.total_variables)]
        for i in range(self.graph_size):
            for j in range(self.graph_size):
                obj[self.get_xij_index(i, j)] = self.graph.matrix[i][j]
        return obj

    def get_ub(self):
        ub = [0 for _ in range(self.total_variables)]
        for song in range(self.songs_amount):
            song_nodes = self.get_nodes_associated_to_song(song)
            for i in song_nodes:
                for j in range(self.graph_size):
                    if j not in song_nodes:
                        ub[self.get_xij_index(i, j)] = 1
        for i in range(self.graph_size):
            ub[self.get_ui_index(i)] = self.graph_size - 1
        return ub
    
    def add_constraints(self):
        self.add_outgoing_constraints()
        self.add_ingoing_constraints()
        self.add_continuous_path_constraints()
        self.add_u_constraints()
    
    def add_outgoing_constraints(self):
        rows = []
        for i in range(self.songs_amount):
            sub_nodes_indices = self.get_nodes_associated_to_song(i)
            ind = []
            for index in sub_nodes_indices:
                ind += [self.get_xij_index(index, j) for j in range(self.graph_size) if j not in sub_nodes_indices]
            rows.append(cplex.SparsePair(ind=ind, val=[1] * len(ind)))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['E'] * len(rows), rhs=[1] * len(rows))
        print ("Added {} outgoing constraints".format(len(rows)))
    
    def add_ingoing_constraints(self):
        rows = []
        for j in range(self.songs_amount):
            sub_nodes_indices = self.get_nodes_associated_to_song(j)
            ind = []
            for index in sub_nodes_indices:
                ind += [self.get_xij_index(i, index) for i in range(self.graph_size) if i not in sub_nodes_indices]
            rows.append(cplex.SparsePair(ind=ind, val=[1] * len(ind)))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['E'] * len(rows), rhs=[1] * len(rows))
        print ("Added {} ingoing constraints".format(len(rows)))

    def add_continuous_path_constraints(self):
        """
        These constraints need to be added because of the existence of subnodes
        """
        rows = []
        for i in range(self.graph_size):
            ind, val = [], []
            for j in range(self.graph_size):
                if i != j:
                    ind += [self.get_xij_index(i, j), self.get_xij_index(j, i)]
                    val += [1, -1]  
            rows.append(cplex.SparsePair(ind=ind, val=val))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['E'] * len(rows), rhs=[0] * len(rows))

    def add_u_constraints(self):
        rows = []
        for i in range(1, self.graph_size):
            for j in range(1, self.graph_size):
                if i != j:
                    ind = [self.get_ui_index(i), self.get_ui_index(j), self.get_xij_index(i, j)]
                    val = [1, -1, self.songs_amount]
                    rows.append(cplex.SparsePair(ind=ind, val=val))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[self.songs_amount - 1] * len(rows))
        print ("Added {} u variables constraints".format(len(rows)))

    def get_nodes_associated_to_song(self, song_index):
        if not song_index:
            return [0]
        song_index -= 1
        return list(range(self.shifts_amount * song_index + 1, self.shifts_amount * (song_index + 1) + 1))

    def get_results(self):
        path = []
        solution_values = self.solver.solution.get_values()
        used_edges = []
        for var in range(self.graph_size ** 2):
            if solution_values[var]:
                used_edges.append(self.get_edge_from_index(var))
        path = self.reconstruct_path(used_edges)
        return path
    
    def get_xij_index(self, i, j):
        return i * self.graph_size + j
    
    def get_edge_from_index(self, index):
        out = index % self.graph_size
        return (index - out) / self.graph_size, out

    def get_ui_index(self, i):
        return self.graph_size ** 2 + i
    
    def reconstruct_path(self, edges):
        edges_path = []
        edges_path.append(edges[0])
        edges.remove(edges[0])
        next_edge = True
        while next_edge:
            next_edge = False
            for edge in edges:
                if edge[0] == edges_path[-1][1]:
                    edges_path.append(edge)
                    edges.remove(edge)
                    next_edge = True
                    break
            
        while len(edges_path) < self.songs_amount - 1:
            for edge in edges:
                if edge[1] == edges_path[0][0]:
                    edges_path = [edge] + edges_path
                    edges.remove(edge)

        node_path = []
        for edge in edges_path[1:]:
            node_path.append(edge[0])

        return node_path
