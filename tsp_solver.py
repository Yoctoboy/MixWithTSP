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

        for i in range(self.graph_size):
            self.graph.matrix[i][i] = 10000000
    
    def create_model(self):
        self.prepare_solver()
        self.add_constraints()
    
    def solve(self):
        self.solver.solve

    def prepare_solver(self):
        self.solver.objective.set_sense(self.solver.objective.sense.minimize)
        obj = self.get_obj()
        ub = self.get_ub()
        types = (self.graph_size ** 2) * [self.solver.variables.type.binary] + \
            self.graph_size * [self.solver.variables.type.integer]
        lb = [0 for _ in range(self.total_variables)]
        self.solver.variables.add(obj=obj, lb=lb, ub=ub, types=types)
    
    def get_obj(self):
        obj = [0 for _ in range(self.total_variables)]
        for i in range(self.graph_size):
            for j in range(self.graph_size):
                obj[self.get_xij_index(i, j)] = self.graph.matrix[i][j]
        return obj

    def get_ub(self):
        ub = [0 for _ in range(self.total_variables)]
        for i in range(self.graph_size):
            for j in range(self.graph_size):
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
        self.add_edges_amount_constraints()
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
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[1] * len(rows))
    
    def add_ingoing_constraints(self):
        rows = []
        for j in range(self.songs_amount):
            sub_nodes_indices = self.get_nodes_associated_to_song(j)
            ind = []
            for index in sub_nodes_indices:
                ind += [self.get_xij_index(i, index) for i in range(self.graph_size) if i not in sub_nodes_indices]
            rows.append(cplex.SparsePair(ind=ind, val=[1] * len(ind)))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[1] * len(rows))

    def add_edges_amount_constraints(self):
        """
        These constraint needs to be added because we want a Hamiltonian path (and not a cycle)
        """

        ind = list(range(self.graph_size ** 2))
        row = [cplex.SparsePair(ind=ind, val=[1] * len(ind))]
        self.solver.linear_constraints.add(lin_expr=row, senses=['E'], rhs=[self.songs_amount - 1])
    
    def add_continuous_path_constraints(self):
        """
        These constraints need to be added because of the existence of subnodes
        """

        rows = []
        for i in range(self.graph_size):
            ind, val = [], []
            for j in range(self.graph_size):
                ind += [self.get_xij_index(i, j), self.get_xij_index(j, i)]
                val += [1, -1]
            rows.append(cplex.SparsePair(ind=ind, val=val))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['E'] * len(rows), rhs=[0] * len(rows))

    
    def add_u_constraints(self):
        rows = []
        for i in range(self.graph_size):
            for j in range(self.graph_size):
                if i != j:
                    ind = [self.get_ui_index(i), self.get_ui_index(j), self.get_xij_index(i, j)]
                    val = [1, -1, self.songs_amount]
                rows.append(cplex.SparsePair(ind=ind, val=val))
        self.solver.linear_constraints.add(lin_expr=rows, senses=['L'] * len(rows), rhs=[self.songs_amount - 1])
    
    def get_nodes_associated_to_song(self, song_index):
        return list(range(self.shifts_amount * song_index, self.shifts_amount * (song_index + 1)))