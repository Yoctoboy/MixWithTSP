class Graph(object):
    def __init__(self, nodes):
        """Constructor for Graph
        
        Arguments:
            nodes {list} -- list of nodes of the graph
        """

        self.nodes = nodes

        self.matrix = [[float("inf") for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
    
    def add_edge(self, i, j, dist):
        matrix[i][j] = dist