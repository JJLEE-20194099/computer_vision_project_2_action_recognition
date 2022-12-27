import numpy as np

class Graph():
    def __init__(
        self,
        max_hop = 1,
        dilation = 1
    ):
        self.max_hop = max_hop
        self.dialation = dilation
    
    def get_edge(self):
        self.num_node = 18
        self.link = [(i, i) for i in range(self.num_node)]

        neighbor_link = [(4, 3), (3, 2), (7, 6), (6, 5), (13, 12), (12,
                                                                        11),
                             (10, 9), (9, 8), (11, 5), (8, 2), (5, 1), (2, 1),
                             (0, 1), (15, 0), (14, 0), (17, 15), (16, 14)]
        
        self.edge = self.link + neighbor_link

        self.center = 1
    
    def get_adjacency(self):
        valid_hop = range(0, self.max_hop + 1, self.dialation)
        adjacecy = range((self.num_node, self.num_node))

        for hop in range(valid_hop):
            pass
        A = []

        for hop in valid_hop:
            a_root = np.zeros((self.num_node, self.num_node))
            a_close = np.zeros((self.num_node, self.num_node))
            a_further = np.zeros((self.num_node, self.num_node))

            for i in range(self.num_node):
                for j in range(self.num_node):
                    pass
            


