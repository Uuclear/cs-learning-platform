# 图的遍历：BFS（广度优先）和 DFS（深度优先）
# BFS像水波纹扩散——一层一层往外荡
# DFS像走迷宫——一条路走到底，撞墙再回头


from collections import deque


class Graph:
    """用邻接表实现的图，支持有向/无向"""

    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed

    def add_edge(self, src, dst):
        """添加一条边"""
        if src not in self.graph:
            self.graph[src] = []
        if dst not in self.graph:
            self.graph[dst] = []
        self.graph[src].append(dst)
        if not self.directed:
            self.graph[dst].append(src)

    def bfs(self, start):
        """
        广度优先搜索（Breadth-First Search）
        核心工具：队列（FIFO先进先出）
        就像往水里扔石头，水波纹一圈一圈往外扩
        """
        if start not in self.graph:
            return []

        visited = set()       # 记录已访问的节点（防止走回头路）
        queue = deque([start]) # 队列：先进先出
        visited.add(start)
        result = []

        while queue:
            vertex = queue.popleft()  # 从队首取出一个节点
            result.append(vertex)

            # 把这个节点的所有未访问邻居加入队列
            for neighbor in self.graph.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start):
        """
        深度优先搜索（Depth-First Search）
        核心工具：栈（LIFO后进先出），或递归
        就像走迷宫：选一条路一直走，走不通了就回头
        """
        if start not in self.graph:
            return []

        visited = set()
        result = []
        stack = [start]  # 栈：后进先出

        while stack:
            vertex = stack.pop()  # 从栈顶取出一个节点
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                # 邻居逆序入栈，保证从左到右的顺序遍历
                for neighbor in reversed(self.graph.get(vertex, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def dfs_recursive(self, start, visited=None):
        """DFS的递归版本——代码更简洁，但深度大了会爆栈"""
        if visited is None:
            visited = set()
        if start not in self.graph:
            return []

        visited.add(start)
        result = [start]

        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                result.extend(self.dfs_recursive(neighbor, visited))

        return result

    def display(self):
        """打印图的结构"""
        for vertex in sorted(self.graph.keys()):
            neighbors = self.graph[vertex]
            print(f"  {vertex} -> {', '.join(str(n) for n in neighbors)}")


# ===== 测试 =====
if __name__ == "__main__":
    # 构建一个图来演示
    # 节点A到J，代表不同的城市
    #
    #       A --- B --- C
    #       |     |     |
    #       D --- E     F
    #       |     |     |
    #       G --- H --- I --- J
    #

    g = Graph(directed=False)  # 无向图
    g.add_edge("A", "B")
    g.add_edge("A", "D")
    g.add_edge("B", "C")
    g.add_edge("B", "E")
    g.add_edge("C", "F")
    g.add_edge("D", "E")
    g.add_edge("D", "G")
    g.add_edge("E", "H")
    g.add_edge("F", "I")
    g.add_edge("G", "H")
    g.add_edge("H", "I")
    g.add_edge("I", "J")

    print("=== 图的结构 ===")
    g.display()

    print("\n=== BFS（广度优先搜索）从A出发 ===")
    bfs_result = g.bfs("A")
    print(f"访问顺序: {' -> '.join(bfs_result)}")
    print("特点：先访问离A最近的邻居，再访问更远的节点")
    print("就像水波纹：A -> (B,D) -> (C,E,G) -> (H,F) -> (I) -> (J)")

    print("\n=== DFS（迭代版）从A出发 ===")
    dfs_result = g.dfs("A")
    print(f"访问顺序: {' -> '.join(dfs_result)}")
    print("特点：一条路走到底，撞墙了再回头")

    print("\n=== DFS（递归版）从A出发 ===")
    dfs_rec_result = g.dfs_recursive("A")
    print(f"访问顺序: {' -> '.join(dfs_rec_result)}")

    print("\n=== BFS vs DFS 对比 ===")
    print(f"BFS 访问顺序: {' -> '.join(bfs_result)}")
    print(f"DFS 访问顺序: {' -> '.join(dfs_result)}")
    print("\nBFS像查字典：从A开始，先查所有A开头的，再查AB开头的...")
    print("DFS像走迷宫：A→B→C→F→I→J，撞墙！回头到I→H→G→D→E")

    # ===== 应用：找最短路径（无权图）=====
    print("\n=== BFS求最短路径：从A到J ===")

    def bfs_shortest_path(graph, start, end):
        """BFS不仅能遍历，还能找到无权图的最短路径"""
        if start not in graph.graph:
            return None

        visited = {start}
        queue = deque([(start, [start])])  # 队列里存(当前节点, 路径)

        while queue:
            vertex, path = queue.popleft()

            if vertex == end:
                return path  # 找到终点，返回路径

            for neighbor in graph.graph.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # 没找到路径

    path = bfs_shortest_path(g, "A", "J")
    if path:
        print(f"最短路径: {' -> '.join(path)}")
        print(f"经过 {len(path) - 1} 条边")
    else:
        print("找不到路径！")

# 注意：BFS/DFS具体访问顺序取决于邻接表中邻居的顺序
# 不同实现可能有细微差异，但BFS保证"按层"访问、DFS保证"深入优先"

# 预期输出:
# === 图的结构 ===
#   A -> B, D
#   B -> A, C, E
#   C -> B, F
#   D -> A, E, G
#   E -> B, D, H
#   F -> C, I
#   G -> D, H
#   H -> E, G, I
#   I -> F, H, J
#   J -> I
#
# === BFS（广度优先搜索）从A出发 ===
# 访问顺序: A -> B -> D -> C -> E -> G -> F -> H -> I -> J
# 特点：先访问离A最近的邻居，再访问更远的节点
# 就像水波纹：A -> (B,D) -> (C,E,G) -> (F,H) -> (I) -> (J)
#
# === DFS（迭代版）从A出发 ===
# 访问顺序: A -> B -> C -> F -> I -> H -> E -> D -> G -> J
# 特点：一条路走到底，撞墙了再回头
#
# === DFS（递归版）从A出发 ===
# 访问顺序: A -> B -> C -> F -> I -> H -> E -> D -> G -> J
#
# === BFS vs DFS 对比 ===
# BFS 访问顺序: A -> B -> D -> C -> E -> G -> F -> H -> I -> J
# DFS 访问顺序: A -> B -> C -> F -> I -> H -> E -> D -> G -> J
#
# BFS像查字典：从A开始，先查所有A开头的，再查AB开头的...
# DFS像走迷宫：选一条路一直走到底
#
# === BFS求最短路径：从A到J ===
# 最短路径: A -> B -> C -> F -> I -> J
# 经过 5 条边
