import cplex


class TSPSolver(object):

    def __init__(self, graph, shifts_amount):
        """
        Constructor for TSPSolver
        
        Arguments:
            graph {Graph} -- Graph of all nodes, containning the matrix
            shifts_amount {int} -- amount of shifts per song
        """

        self.graph = graph
        self.graph_size = len(self.graph.nodes)
        self.shifts_amount = shifts_amount
        self.songs_amount = self.graph_size / self.shifts_amount
        self.total_variables = self.graph_size * (self.graph_size + 1)
        self.solver = cplex.Cplex()
        print(self.shifts_amount, self.songs_amount)

        for i in range(self.graph_size):
            self.graph.matrix[i][i] = 10000000
    
    def create_model(self):
        self.prepare_solver()
        self.add_constraints()
    
    def solve(self):
        self.solver.write("mod.lp")
        self.solver.solve()
        return self.get_results()

    def prepare_solver(self):
        self.solver.objective.set_sense(self.solver.objective.sense.minimize)
        obj = self.get_obj()
        ub = self.get_ub()
        types = (self.graph_size ** 2) * [self.solver.variables.type.binary] + \
            self.graph_size * [self.solver.variables.type.integer]
        lb = [0 for _ in range(self.total_variables)]
        self.solver.variables.add(obj=obj, lb=lb, ub=ub, types=types)
        colnames = []
        for start_song in range(self.songs_amount):
            for i in self.get_nodes_associated_to_song(start_song):
                for end_song in range(self.songs_amount):
                    for j in self.get_nodes_associated_to_song(end_song):
                        colnames.append("x_{}_{}__{}_{}".format(start_song, i % self.shifts_amount, end_song, j % self.shifts_amount))
        for i in range(self.graph_size):
            colnames.append("u_{}".format(i))
        self.solver.variables.set_names([(i, colnames[i]) for i in range(self.total_variables)])
    
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
    
    def get_xij_index(self, i, j):
        return i * self.graph_size + j
    
    def get_ui_index(self, i):
        return self.graph_size ** 2 + i
    
    def add_constraints(self):
        self.add_outgoing_constraints()
        self.add_ingoing_constraints()
        self.add_edges_amount_constraint()
        self.add_u_constraints()
    
    def add_outgoing_constraints(self):
        rows = []
        for i in range(self.songs_amount):
            sub_nodes_indices = self.get_nodes_associated_to_song(i)
            ind = []
            for index in sub_nodes_indices:
                ind += [self.get_xij_index(index, j) for j in range(self.graph_size) if j not in sub_nodes_indices]
            rows.append(cplex.SparsePair(ind=ind, val=[1] * len(ind)))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[1] * len(rows))
        print ("Added {} outgoing constraints".format(len(rows)))
    
    def add_ingoing_constraints(self):
        rows = []
        for j in range(self.songs_amount):
            sub_nodes_indices = self.get_nodes_associated_to_song(j)
            ind = []
            for index in sub_nodes_indices:
                ind += [self.get_xij_index(i, index) for i in range(self.graph_size) if i not in sub_nodes_indices]
            rows.append(cplex.SparsePair(ind=ind, val=[1] * len(ind)))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[1] * len(rows))
        print ("Added {} ingoing constraints".format(len(rows)))

    def add_edges_amount_constraint(self):
        """
        These constraint needs to be added because we want a Hamiltonian path (and not a cycle)
        """

        ind = list(range(self.graph_size ** 2))
        row = [cplex.SparsePair(ind=ind, val=[1] * len(ind))]
        self.solver.linear_constraints.add(lin_expr=row, senses=['E'], rhs=[self.songs_amount - 1])
        print ("Added 1 edges amount constraints")

    def add_u_constraints(self):
        rows = []
        for i in range(self.graph_size):
            for j in range(self.graph_size):
                if i != j:
                    ind = [self.get_ui_index(i), self.get_ui_index(j), self.get_xij_index(i, j)]
                    val = [1, -1, self.songs_amount]
                    rows.append(cplex.SparsePair(ind=ind, val=val))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[self.songs_amount - 1] * len(rows))
        print ("Added {} u variables constraints".format(len(rows)))

    def get_nodes_associated_to_song(self, song_index):
        return list(range(self.shifts_amount * song_index, self.shifts_amount * (song_index + 1)))

    def get_results(self):
        path = []
        solution_values = self.solver.solution.get_values()
        u_values = [solution_values[self.get_ui_index(i)] for i in range(self.graph_size)]
        return u_values