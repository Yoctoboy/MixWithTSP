class Graph(object):
    def __init__(self, nodes):
        """Constructor for Graph
        
        Arguments:
            nodes {list} -- list of nodes of the graph
        """

        self.nodes = nodes
        self.matrix = [[float("inf") for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
    
    def __repr__(self):
        res = ""
        #for node in self.nodes:
        #    res += "Node {} (index={}) with shift {}\n".format(node["name"], node["index"], node["shift"])
        for matrix_line in self.matrix:
            for element in matrix_line:
                to_add = str(element) + "," + (" " * (5 -len(str(element))))
                res += to_add
            res += "\n"
        return res
    
    def add_edge(self, i, j, dist):
        self.matrix[i][j] = dist