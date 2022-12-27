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
            
def get_hop_distance(num_node, edge, max_hop = 1):
    A = np.zeros((num_node, num_node))

    for i, j in edge:
        A[i, j] = 1
        A[j, i] = 1

    hop_dis = np.zeros((num_node, num_node)) + np.inf
    transfer_mat = [np.linalg.matrix_power(A, d) for d in range(max_hop + 1)]
    arrive_mat = (np.stack(transfer_mat) > 0)
    for d in range(max_hop, -1, -1):
        hop_dis[arrive_mat[d]] = d
    
    # Nếu i, j là hàng xóm => hop_dis[i, j] = 1
    # Nếu i là node=> hop_dis[i, i] = 0
    # Nếu  ngược lại => hop_dis[i, j] =  dương vô cùng
    
    return hop_dis