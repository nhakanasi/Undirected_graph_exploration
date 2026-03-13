class UnionFind:
    """A data structure for maintaining disjoint sets."""
    def __init__(self, nodes):
        """Initialize the structure for a set of nodes.
        
        ``nodes`` should be an iterable of node labels.
        """
        self.parent = {node: node for node in nodes}
        self.num_sets = len(nodes)

    def find(self, i):
        """Find the representative (root) of the set containing ``i``."""
        if self.parent[i] == i:
            return i
        # Path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Merge the sets containing ``i`` and ``j``."""
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_j] = root_i
            self.num_sets -= 1
            return True
        return False
