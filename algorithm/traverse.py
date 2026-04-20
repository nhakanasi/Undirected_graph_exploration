from collections import deque

def BFS(graph, start=None, visit_all=True):
    order = []
    seen = set()
    nodes = list(graph.all_nodes())

    if not nodes:
        return order, seen

    if start is None or start not in nodes:
        start = nodes[0]

    seeds = [start] + [node for node in nodes if node != start]
    for seed in seeds:
        if seed not in seen:
            q = deque([seed])
            seen.add(seed)
            while q:
                u = q.popleft()
                order.append(u)
                for v in graph.neighbors(u):
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
            if not visit_all:
                break

    return order, seen


def DFS(graph, start=None, visit_all=True):
    order = []
    seen = set()
    nodes = list(graph.all_nodes())

    if not nodes:
        return order, seen

    if start is None or start not in nodes:
        start = nodes[0]

    seeds = [start] + [node for node in nodes if node != start]
    for seed in seeds:
        if seed not in seen:
            stack = [seed]
            seen.add(seed)
            while stack:
                u = stack.pop()
                order.append(u)
                for v in reversed(list(graph.neighbors(u))):
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
            if not visit_all:
                break

    return order, seen