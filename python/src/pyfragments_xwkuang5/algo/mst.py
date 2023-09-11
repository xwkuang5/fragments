import heapq
import numpy as np


class disjoint_set:
    """A data structure for checking whether two elements belong to the same set
    """

    def __init__(self, size):
        self.parray = np.zeros(size, dtype=np.uint8)
        self.rank = np.zeros(size, dtype=np.uint8)

    def make_set(self, v):
        self.parray[v] = v

    def find_set(self, v):
        if self.parray[v] == v:
            return v
        else:
            # With path compression
            ret = self.find_set(self.parray[v])
            self.parray[v] = ret
            return ret

    def union_set(self, i, j):
        # With union by rank
        pi = self.find_set(i)
        pj = self.find_set(j)
        ri = self.rank[pi]
        rj = self.rank[pj]
        if pi != pj:
            if ri < rj:
                self.parray[pi] = pj
            elif ri > rj:
                self.parray[pj] = pi
            else:
                self.parray[pi] = pj
                self.rank[pj] += 1


class Graph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.queue = []

    def add_edge(self, i, j, v):
        heapq.heappush(self.queue, (v, (i, j)))

    def build_mst_kruskals(self):
        union_find_ds = disjoint_set(self.num_nodes)
        queue_copy = self.queue.copy()
        for i in range(self.num_nodes):
            union_find_ds.make_set(i)

        mst_cost = 0

        while len(queue_copy) != 0:
            (v, (i, j)) = heapq.heappop(queue_copy)
            if union_find_ds.find_set(i) != union_find_ds.find_set(j):
                union_find_ds.union_set(i, j)
                mst_cost += v
                print("add edge (%d, %d) to MST" % (i, j))

        return mst_cost


g = Graph(5)
g.add_edge(0, 1, 2)
g.add_edge(0, 2, 2)
g.add_edge(1, 2, 3)
g.add_edge(0, 3, 4)
g.add_edge(1, 3, 2)
g.add_edge(1, 4, 3)
g.add_edge(0, 4, 1)
print("cost of mst: %d" % g.build_mst_kruskals())
