from collections import defaultdict
from collections import deque


class DirectedGraph:
    def __init__(self, V):

        self.V = list(range(V))

        self.edges = defaultdict(list)

    def add_edges(self, u, v):

        self.edges[u].append(v)

    def bi_search(self, src, dst):
        def intersect(src_visited, dst_visited):

            for i in range(len(src_visited)):
                if src_visited[i] and dst_visited[i]:
                    return i
            return -1

        def one_step_bfs(queue, visited, edges, parents):

            u = queue.popleft()

            visited[u] = True

            for v in edges[u]:
                if not visited[v]:
                    parents[v] = u
                    queue.append(v)

        def get_path(node, src_parents, dst_parents):

            to_path = [node]

            parent = dst_parents[node]

            while parent != -1:
                to_path.append(parent)
                parent = dst_parents[parent]

            from_path = []

            parent = src_parents[node]

            while parent != -1:
                from_path.append(parent)
                parent = src_parents[parent]

            return from_path[::-1] + to_path

        src_queue = deque()
        dst_queue = deque()

        src_parents = [None] * len(self.V)
        dst_parents = [None] * len(self.V)

        src_visited = [False] * len(self.V)
        dst_visited = [False] * len(self.V)

        src_parents[src] = -1
        dst_parents[dst] = -1

        src_queue.append(src)
        dst_queue.append(dst)

        while len(src_queue) != 0 and len(dst_queue) != 0:

            one_step_bfs(src_queue, src_visited, self.edges, src_parents)
            one_step_bfs(dst_queue, dst_visited, self.edges, dst_parents)

            node = intersect(src_visited, dst_visited)

            if node != -1:
                return get_path(node, src_parents, dst_parents)

        return -1
