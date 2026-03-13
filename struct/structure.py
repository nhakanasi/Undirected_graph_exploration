import re
from collections import defaultdict
from abc import abstractmethod
class UndirectedGraph:
    def __init__(self, data_path):
        """
        Init the class to read txt file in the format of roadNet, i.e
        1st line: garbage
        2nd line: state network
        3rd line: node edges
        4rd line: the format of the file
        """
        with open(data_path, "r") as f:
            f.readline(); f.readline()
            header = f.readline().strip()
            m = re.search(r"Nodes:\s*(\d+)\s+Edges:\s*(\d+)", header)
            if m:
                self.node_count = int(m.group(1))
                self.edge_count = int(m.group(2))
            f.readline() 
            self.data = f.readlines()

    
    @abstractmethod
    def get_struct(self):
        """
        An abstract function to return the data represented in data structure
        """
        
    @abstractmethod
    def neighbors(self, node):
        """Return an iterable of neighbours for a given node."""
        
    @abstractmethod
    def all_nodes(self):
        """Return an iterable of all nodes in the graph."""

    @abstractmethod
    def get_edges(self):
        """Return an iterable of all edges in the graph as (u, v) tuples."""



class AdjacencyMatrix(UndirectedGraph):
    def __init__(self, data_path):
        super().__init__(data_path)

        node_set = set()
        edges = []

        for line in self.data:
            parts = line.split()
            if len(parts) != 2:
                continue

            start = int(parts[0])
            end = int(parts[1])

            node_set.add(start)
            node_set.add(end)
            edges.append((start, end))

        self.nodes = sorted(node_set)
        self.node_set = set(self.nodes)

        self.mapped = {node: idx for idx, node in enumerate(self.nodes)}
        self.node_count = len(self.nodes)
        self.matrix = [[0] * self.node_count for _ in range(self.node_count)]

        for start, end in edges:
            i = self.mapped[start]
            j = self.mapped[end]
            self.matrix[i][j] = 1
            self.matrix[j][i] = 1

    def get_struct(self):
        return self.matrix, self.nodes

    def neighbors(self, node):
        idx = self.mapped[node]
        return [self.nodes[j] for j, val in enumerate(self.matrix[idx]) if val]

    def all_nodes(self):
        return self.nodes

    def get_edges(self):
        edges = []
        for i in range(self.node_count):
            for j in range(i + 1, self.node_count):
                if self.matrix[i][j]:
                    edges.append((self.nodes[i], self.nodes[j]))
        return edges

class AdjencyDict(UndirectedGraph):
    def __init__(self, data_path):
        super().__init__(data_path)
        self.adj_list = defaultdict(list)
        for line in self.data:
            parts = line.split()
            if len(parts) != 2:
                continue

            start = int(parts[0])
            end = int(parts[1])

            self.adj_list[start].append(end)
            self.adj_list[end].append(start)
        
        self.node = self.adj_list.keys()
    
    def get_struct(self):
        return self.adj_list, self.node

    def neighbors(self, node):
        return self.adj_list.get(node, [])

    def all_nodes(self):
        return list(self.node)

    def get_edges(self):
        edges = set()
        for u, neighbors in self.adj_list.items():
            for v in neighbors:
                if u < v:
                    edges.add((u, v))
        return list(edges)
