from collections import deque
def BFS(graph, start):
    order = []
    q = deque([start])
    seen = {start}

    while q:
        u = q.popleft()
        order.append(u)
        for v in graph.neighbors(u):
            if v not in seen:
                seen.add(v)
                q.append(v)

    return order, seen


def DFS(graph, start):
    order = []
    stack = [start]
    seen = {start}

    while stack:
        u = stack.pop()
        order.append(u)
        for v in reversed(list(graph.neighbors(u))):
            if v not in seen:
                seen.add(v)
                stack.append(v)

    return order, seen