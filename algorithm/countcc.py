from algorithm.traverse import BFS
from struct.union_find import UnionFind

def count_connected_components_bfs(graph):
    seen = set()
    count = 0
    for node in graph.all_nodes():
        if node not in seen:
            count += 1
            _, component_nodes = BFS(graph, node)
            seen.update(component_nodes)
    return count

def count_connected_components_uf(graph):
    nodes = graph.all_nodes()
    uf = UnionFind(nodes)

    for u, v in graph.get_edges():
        uf.union(u, v)

    return uf.num_sets
