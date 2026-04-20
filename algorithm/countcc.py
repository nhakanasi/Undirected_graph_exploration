from collections import deque
from struct.union_find import UnionFind

def count_connected_components_bfs(graph):
    nodes = list(graph.all_nodes())
    if not nodes:
        return 0

    seen = set()
    count = 0
    neighbors = graph.neighbors

    for node in nodes:
        if node in seen:
            continue

        count += 1
        q = deque([node])
        seen.add(node)

        while q:
            u = q.popleft()
            for v in neighbors(u):
                if v not in seen:
                    seen.add(v)
                    q.append(v)

    return count

def count_connected_components_uf(graph):
    nodes = graph.all_nodes()
    uf = UnionFind(nodes)

    for u, v in graph.get_edges():
        uf.union(u, v)

    return uf.num_sets
