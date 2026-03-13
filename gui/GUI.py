import tkinter as tk
from tkinter import filedialog
import os
import sys
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from struct.structure import AdjencyDict, AdjacencyMatrix
from algorithm.traverse import BFS, DFS
from algorithm.countcc import count_connected_components_bfs, count_connected_components_uf

class GraphExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Exploration GUI")
        self.root.geometry("1000x650")
        self.root.configure(bg="#3b3b3b")
        self.graph = None
        self.graph_dict = None
        self.graph_matrix = None
        self.structure_mode = tk.StringVar(value="dict")

        self.left_frame = tk.Frame(self.root, bg="#535353", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.left_frame.pack_propagate(False)

        tk.Label(self.left_frame, text="1. Mode", bg="#535353", fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(15, 5))
        
        btn_frame1 = tk.Frame(self.left_frame, bg="#535353")
        btn_frame1.pack(fill=tk.X, padx=10)
        

        self.btn_load = tk.Button(btn_frame1, text="Load Data", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.load_data)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_show_data = tk.Button(btn_frame1, text="Show Data", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.show_data)
        self.btn_show_data.grid(row=0, column=1, padx=5, pady=5)

        mode_frame = tk.Frame(self.left_frame, bg="#535353")
        mode_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        tk.Label(mode_frame, text="Structure:", bg="#535353", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        self.radio_dict = tk.Radiobutton(mode_frame, text="Dict", variable=self.structure_mode, value="dict", bg="#535353", fg="white", selectcolor="#3f3f3f", activebackground="#535353", activeforeground="white", command=self._sync_active_graph)
        self.radio_dict.pack(side=tk.LEFT, padx=(8, 4))
        self.radio_matrix = tk.Radiobutton(mode_frame, text="Matrix", variable=self.structure_mode, value="matrix", bg="#535353", fg="white", selectcolor="#3f3f3f", activebackground="#535353", activeforeground="white", command=self._sync_active_graph)
        self.radio_matrix.pack(side=tk.LEFT, padx=4)
        
        tk.Label(self.left_frame, text="2. Process", bg="#535353", fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        btn_frame2 = tk.Frame(self.left_frame, bg="#535353")
        btn_frame2.pack(fill=tk.X, padx=10)
        
        self.btn_bfs = tk.Button(btn_frame2, text="BFS (3 Steps)", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.run_bfs)
        self.btn_bfs.grid(row=0, column=0, padx=5, pady=5)
        self.btn_dfs = tk.Button(btn_frame2, text="DFS (3 Steps)", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.run_dfs)
        self.btn_dfs.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_cc_bfs = tk.Button(btn_frame2, text="CC by BFS", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.count_cc_bfs)
        self.btn_cc_bfs.grid(row=1, column=0, padx=5, pady=5)
        self.btn_cc_uf = tk.Button(btn_frame2, text="CC by UF", width=12, bg="#dddddd", font=("Arial", 9, "bold"), command=self.count_cc_uf)
        self.btn_cc_uf.grid(row=1, column=1, padx=5, pady=5)
        self.btn_cc = tk.Button(btn_frame2, text="CC Compare", width=27, bg="#dddddd", font=("Arial", 9, "bold"), command=self.count_cc)
        self.btn_cc.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.left_frame, text="3. Notification", bg="#535353", fg="white", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        self.console = tk.Text(self.left_frame, bg="#dddddd", font=("Consolas", 10), wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 15))

        self.right_frame = tk.Frame(self.root, bg="#4b4b4b")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        self.visual_canvas = tk.Canvas(self.right_frame, bg="#333333", highlightthickness=0)
        self.visual_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_visual("Visualization area initialized. Waiting for data...")

    def log_console(self, text):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.update()

    def log_visual(self, text):
        self.clear_canvas()
        self.visual_canvas.create_text(20, 20, anchor="nw", fill="#00ff00", font=("Consolas", 14), text=text)

    def clear_canvas(self):
        self.visual_canvas.delete("all")

    def draw_node(self, x, y, label, fill="#2d6cdf"):
        r = 24
        self.visual_canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline="#dddddd", width=2)
        self.visual_canvas.create_text(x, y, text=str(label), fill="white", font=("Arial", 10, "bold"))

    def draw_edge(self, x1, y1, x2, y2):
        self.visual_canvas.create_line(x1, y1, x2, y2, fill="#cccccc", width=2)

    def _order_tree_nodes(self, order, branching, depth):
        max_nodes = 0
        level_size = 1
        for _ in range(depth):
            max_nodes += level_size
            level_size *= branching
        return order[:max_nodes]

    def draw_order_tree(self, order, branching, depth, title, node_fill):
        self.clear_canvas()
        self.visual_canvas.create_text(30, 30, anchor="nw", fill="#00ff00", font=("Consolas", 12, "bold"), text=title)

        tree_nodes = self._order_tree_nodes(order, branching, depth)
        if not tree_nodes:
            self.visual_canvas.create_text(30, 80, anchor="nw", fill="white", font=("Consolas", 11), text="No nodes to draw")
            return

        canvas_w = max(self.visual_canvas.winfo_width(), 700)
        top_y = 90
        level_gap = 110
        placed = []
        index = 0

        for level in range(depth):
            level_count = branching ** level
            y = top_y + level * level_gap
            segment = canvas_w / (level_count + 1)
            row = []
            for i in range(level_count):
                if index >= len(tree_nodes):
                    break
                x = int(segment * (i + 1))
                row.append((x, y, tree_nodes[index], index))
                index += 1
            placed.append(row)
            if index >= len(tree_nodes):
                break

        for level in range(len(placed) - 1):
            for px, py, _, parent_idx in placed[level]:
                for child_offset in range(1, branching + 1):
                    child_idx = parent_idx * branching + child_offset
                    for cx, cy, _, global_idx in placed[level + 1]:
                        if global_idx == child_idx:
                            self.draw_edge(px, py, cx, cy)
                            break

        for row in placed:
            for x, y, label, _ in row:
                self.draw_node(x, y, label, fill=node_fill)

    def _dfs_with_parent(self, graph, start):
        order = []
        stack = [start]
        seen = {start}
        parent = {start: None}

        while stack:
            u = stack.pop()
            order.append(u)
            for v in reversed(list(graph.neighbors(u))):
                if v not in seen:
                    seen.add(v)
                    parent[v] = u
                    stack.append(v)

        return order, parent

    def draw_parent_tree(self, parent, order, depth, title, node_fill):
        self.clear_canvas()
        self.visual_canvas.create_text(30, 30, anchor="nw", fill="#00ff00", font=("Consolas", 12, "bold"), text=title)

        if not order:
            self.visual_canvas.create_text(30, 80, anchor="nw", fill="white", font=("Consolas", 11), text="No nodes to draw")
            return

        max_nodes = sum(2 ** i for i in range(depth))
        subset = order[:max_nodes]
        subset_set = set(subset)

        depth_map = {}
        for node in subset:
            d = 0
            cur = node
            while parent.get(cur) is not None and parent[cur] in subset_set:
                d += 1
                cur = parent[cur]
            depth_map[node] = d

        levels = []
        for d in range(depth):
            levels.append([n for n in subset if depth_map.get(n, 0) == d])

        canvas_w = max(self.visual_canvas.winfo_width(), 700)
        top_y = 90
        level_gap = 95
        coords = {}

        for d, row in enumerate(levels):
            if not row:
                continue
            y = top_y + d * level_gap
            segment = canvas_w / (len(row) + 1)
            for i, node in enumerate(row):
                x = int(segment * (i + 1))
                coords[node] = (x, y)

        for node in subset:
            p = parent.get(node)
            if p is not None and p in coords and node in coords:
                px, py = coords[p]
                cx, cy = coords[node]
                self.draw_edge(px, py, cx, cy)

        for node in subset:
            if node in coords:
                x, y = coords[node]
                self.draw_node(x, y, node, fill=node_fill)

    def _sync_active_graph(self):
        if self.structure_mode.get() == "matrix" and self.graph_matrix is not None:
            self.graph = self.graph_matrix
        elif self.graph_dict is not None:
            self.graph = self.graph_dict

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select Graph Text File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        
        start_t = time.perf_counter()
        self.log_console("Loading data...")
        try:
            self.graph_dict = AdjencyDict(file_path)
            self.graph_matrix = None

            if self.graph_dict.node_count > 20000:
                self.structure_mode.set("dict")
                self.radio_matrix.config(state=tk.DISABLED)
                self.log_console("Node count > 20000: Matrix mode disabled. Using Dict mode only.")
            else:
                self.radio_matrix.config(state=tk.NORMAL)
                try:
                    self.graph_matrix = AdjacencyMatrix(file_path)
                    self.log_console("Matrix structure is available for this dataset.")
                except Exception as matrix_error:
                    self.log_console(f"Matrix build skipped: {matrix_error}")

            self._sync_active_graph()
            self.log_console(f"Successfully loaded data!")
            self.log_console(f"Total Nodes: {self.graph_dict.node_count}")
            self.log_console(f"Total Edges: {self.graph_dict.edge_count}")
            self.log_console(f"Load time: {time.perf_counter() - start_t:.4f}s")
            self.log_visual(f"File loaded: {os.path.basename(file_path)}\nMode: {self.structure_mode.get().upper()}\nReady for operations.")
        except Exception as e:
            self.log_console(f"Error loading graph: {e}")

    def show_data(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return

        start_t = time.perf_counter()
        self.clear_canvas()
        if self.structure_mode.get() == "matrix" and self.graph_matrix is not None:
            matrix, nodes = self.graph_matrix.get_struct()
            n = min(3, len(nodes))
            if n == 0:
                self.log_console("Graph is empty.")
                self.log_visual("No data to visualize.")
                return

            cell = 70
            ox, oy = 140, 120
            self.visual_canvas.create_text(30, 30, anchor="nw", fill="#00ff00", font=("Consolas", 12, "bold"), text="3x3 Matrix Preview")
            for i in range(n):
                self.visual_canvas.create_text(ox - 25, oy + i * cell + cell / 2, text=str(nodes[i]), fill="white", font=("Arial", 10, "bold"))
                self.visual_canvas.create_text(ox + i * cell + cell / 2, oy - 25, text=str(nodes[i]), fill="white", font=("Arial", 10, "bold"))
                for j in range(n):
                    x1 = ox + j * cell
                    y1 = oy + i * cell
                    x2 = x1 + cell
                    y2 = y1 + cell
                    self.visual_canvas.create_rectangle(x1, y1, x2, y2, outline="#bbbbbb", width=2)
                    self.visual_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(matrix[i][j]), fill="#7dff7d", font=("Consolas", 16, "bold"))

            self.log_console("Displayed 3x3 matrix preview.")
        else:
            adj_dict, _ = self.graph_dict.get_struct()
            items = list(adj_dict.items())[:5]
            self.visual_canvas.create_text(30, 30, anchor="nw", fill="#00ff00", font=("Consolas", 12, "bold"), text="Dictionary (Linked-List Style) - First 5")

            row_y = 90
            row_gap = 90
            for node, neighbors in items:
                self.visual_canvas.create_rectangle(40, row_y - 22, 110, row_y + 22, fill="#5c2d91", outline="#dddddd")
                self.visual_canvas.create_text(75, row_y, text=str(node), fill="white", font=("Arial", 10, "bold"))

                x = 145
                for nei in neighbors[:4]:
                    self.visual_canvas.create_line(x - 15, row_y, x, row_y, fill="#cccccc", width=2, arrow=tk.LAST)
                    self.visual_canvas.create_rectangle(x, row_y - 18, x + 70, row_y + 18, fill="#2d6cdf", outline="#dddddd")
                    self.visual_canvas.create_text(x + 35, row_y, text=str(nei), fill="white", font=("Arial", 9, "bold"))
                    x += 95

                if len(neighbors) > 4:
                    self.visual_canvas.create_text(x, row_y, text="...", fill="#dddddd", font=("Arial", 12, "bold"))

                row_y += row_gap

            self.log_console("Displayed dictionary linked-list style preview (first 5 items).")
            self.log_console(f"Show data time: {time.perf_counter() - start_t:.4f}s")

    def run_bfs(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return

        nodes = self.graph.all_nodes()
        if not nodes:
            self.log_console("Graph is empty.")
            return
            
        start_t = time.perf_counter()
        start_node = nodes[0]
        self.log_console(f"Running BFS starting at node [{start_node}]...")
        order, _ = BFS(self.graph, start_node)

        self.draw_order_tree(order, branching=3, depth=2, title=f"BFS tree from order (first nodes, start={start_node})", node_fill="#e67e22")

        steps = min(3, len(order))
        for i in range(steps):
            self.visual_canvas.create_text(30, 450 + i * 28, anchor="nw", fill="white", font=("Consolas", 11), text=f"Step {i + 1}: visit {order[i]}")

        self.log_console(f"BFS Complete. Visited {len(order)} nodes.")
        self.log_console(f"BFS time: {time.perf_counter() - start_t:.4f}s")

    def run_dfs(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return

        nodes = self.graph.all_nodes()
        if not nodes:
            self.log_console("Graph is empty.")
            return
            
        start_t = time.perf_counter()
        start_node = nodes[0]
        self.log_console(f"Running DFS starting at node [{start_node}]...")
        order, parent = self._dfs_with_parent(self.graph, start_node)

        self.draw_parent_tree(parent, order, depth=3, title=f"DFS parent tree (depth 3, start={start_node})", node_fill="#1abc9c")

        steps = min(3, len(order))
        for i in range(steps):
            self.visual_canvas.create_text(30, 450 + i * 28, anchor="nw", fill="white", font=("Consolas", 11), text=f"Step {i + 1}: visit {order[i]}")

        if steps:
            seq = " -> ".join(str(order[i]) for i in range(steps))
            self.visual_canvas.create_text(30, 420, anchor="nw", fill="#ffd166", font=("Consolas", 11, "bold"), text=f"Visit sequence: {seq}")

        self.log_console(f"DFS Complete. Visited {len(order)} nodes.")
        self.log_console(f"DFS time: {time.perf_counter() - start_t:.4f}s")

    def count_cc(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return
            
        self.log_console("Calculating Connected Components...")
        self.log_visual("Calculating Connected Components...")

        bfs_t0 = time.perf_counter()
        cc_bfs = count_connected_components_bfs(self.graph)
        bfs_dt = time.perf_counter() - bfs_t0

        uf_t0 = time.perf_counter()
        cc_uf = count_connected_components_uf(self.graph)
        uf_dt = time.perf_counter() - uf_t0

        self.log_console(f"CC (BFS): {cc_bfs} | time: {bfs_dt:.4f}s")
        self.log_console(f"CC (Union-Find): {cc_uf} | time: {uf_dt:.4f}s")
        self.clear_canvas()
        self.visual_canvas.create_text(40, 70, anchor="nw", fill="#00ff00", font=("Consolas", 16, "bold"), text="Connected Component Result")
        self.visual_canvas.create_text(40, 130, anchor="nw", fill="white", font=("Consolas", 14), text=f"BFS: {cc_bfs} ({bfs_dt:.4f}s)")
        self.visual_canvas.create_text(40, 170, anchor="nw", fill="white", font=("Consolas", 14), text=f"Union-Find: {cc_uf} ({uf_dt:.4f}s)")

    def count_cc_bfs(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return

        self.log_console("Calculating Connected Components by BFS...")
        t0 = time.perf_counter()
        cc_bfs = count_connected_components_bfs(self.graph)
        dt = time.perf_counter() - t0
        self.log_console(f"CC (BFS): {cc_bfs} | time: {dt:.4f}s")
        self.clear_canvas()
        self.visual_canvas.create_text(40, 70, anchor="nw", fill="#00ff00", font=("Consolas", 16, "bold"), text="Connected Component Result")
        self.visual_canvas.create_text(40, 130, anchor="nw", fill="white", font=("Consolas", 14), text=f"Algorithm: BFS")
        self.visual_canvas.create_text(40, 170, anchor="nw", fill="white", font=("Consolas", 14), text=f"Total CC: {cc_bfs}")
        self.visual_canvas.create_text(40, 210, anchor="nw", fill="white", font=("Consolas", 14), text=f"Time: {dt:.4f}s")

    def count_cc_uf(self):
        if not self.graph:
            self.log_console("No graph loaded. Please load data first.")
            return

        self.log_console("Calculating Connected Components by Union-Find...")
        t0 = time.perf_counter()
        cc_uf = count_connected_components_uf(self.graph)
        dt = time.perf_counter() - t0
        self.log_console(f"CC (Union-Find): {cc_uf} | time: {dt:.4f}s")
        self.clear_canvas()
        self.visual_canvas.create_text(40, 70, anchor="nw", fill="#00ff00", font=("Consolas", 16, "bold"), text="Connected Component Result")
        self.visual_canvas.create_text(40, 130, anchor="nw", fill="white", font=("Consolas", 14), text=f"Algorithm: Union-Find")
        self.visual_canvas.create_text(40, 170, anchor="nw", fill="white", font=("Consolas", 14), text=f"Total CC: {cc_uf}")
        self.visual_canvas.create_text(40, 210, anchor="nw", fill="white", font=("Consolas", 14), text=f"Time: {dt:.4f}s")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphExplorerApp(root)
    root.mainloop()

