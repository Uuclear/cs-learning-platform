# 图的两种表示方法：邻接矩阵 vs 邻接表
# 就像社交网络：矩阵是"谁认识谁"的大表格，表是"每个人的好友列表"


class AdjacencyMatrix:
    """
    邻接矩阵表示法
    用一个二维数组记录节点之间的连接关系
    适合稠密图（边很多的情况）
    """

    def __init__(self, num_vertices):
        # 初始化一个 num_vertices x num_vertices 的矩阵，全部填0
        # 0表示不相连，1表示相连（无权图）
        self.num_vertices = num_vertices
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, src, dst, weight=1):
        """添加一条从src到dst的边，weight是权重（默认1）"""
        if 0 <= src < self.num_vertices and 0 <= dst < self.num_vertices:
            self.matrix[src][dst] = weight

    def add_undirected_edge(self, v1, v2, weight=1):
        """添加无向边：v1连v2，v2也连v1"""
        self.add_edge(v1, v2, weight)
        self.add_edge(v2, v1, weight)

    def has_edge(self, src, dst):
        """查询两个节点是否相连"""
        return self.matrix[src][dst] != 0

    def get_neighbors(self, vertex):
        """获取某个节点的所有邻居"""
        neighbors = []
        for i in range(self.num_vertices):
            if self.matrix[vertex][i] != 0:
                neighbors.append((i, self.matrix[vertex][i]))
        return neighbors

    def display(self):
        """打印矩阵"""
        print("   " + "  ".join(f"v{i}" for i in range(self.num_vertices)))
        for i in range(self.num_vertices):
            print(f"v{i} " + "  ".join(f"{self.matrix[i][j]}" for j in range(self.num_vertices)))


class AdjacencyList:
    """
    邻接表表示法
    用字典记录每个节点的邻居列表
    适合稀疏图（边不多的情况），省空间
    """

    def __init__(self):
        # 用字典：key是节点，value是(邻居, 权重)的列表
        self.graph = {}

    def add_vertex(self, vertex):
        """添加一个节点（孤立节点也可以）"""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, src, dst, weight=1):
        """添加一条有向边"""
        if src not in self.graph:
            self.graph[src] = []
        if dst not in self.graph:
            self.graph[dst] = []
        self.graph[src].append((dst, weight))

    def add_undirected_edge(self, v1, v2, weight=1):
        """添加无向边"""
        self.add_edge(v1, v2, weight)
        self.add_edge(v2, v1, weight)

    def has_edge(self, src, dst):
        """查询两个节点是否相连"""
        if src not in self.graph:
            return False
        return any(neighbor == dst for neighbor, _ in self.graph[src])

    def get_neighbors(self, vertex):
        """获取某个节点的所有邻居"""
        return self.graph.get(vertex, [])

    def display(self):
        """打印邻接表"""
        for vertex in sorted(self.graph.keys()):
            neighbors = self.graph[vertex]
            neighbor_str = ", ".join(f"({n}, w={w})" for n, w in neighbors)
            print(f"  {vertex} -> {neighbor_str if neighbor_str else '(无邻居)'}")


# ===== 测试 =====
if __name__ == "__main__":
    # 用一个简单的社交网络来演示
    # 0=小明, 1=小红, 2=小刚, 3=小丽, 4=小王
    # 关系：小明认识小红和小刚，小红认识小刚和小丽，小刚认识小丽，小丽认识小王

    print("=== 邻接矩阵表示法 ===")
    matrix = AdjacencyMatrix(5)
    matrix.add_undirected_edge(0, 1)  # 小明-小红
    matrix.add_undirected_edge(0, 2)  # 小明-小刚
    matrix.add_undirected_edge(1, 2)  # 小红-小刚
    matrix.add_undirected_edge(1, 3)  # 小红-小丽
    matrix.add_undirected_edge(2, 3)  # 小刚-小丽
    matrix.add_undirected_edge(3, 4)  # 小丽-小王
    matrix.display()

    print(f"\n查询: 小明(0)和小红(1)是否相连? {matrix.has_edge(0, 1)}")
    print(f"查询: 小明(0)和小王(4)是否相连? {matrix.has_edge(0, 4)}")
    print(f"小明(0)的朋友: {matrix.get_neighbors(0)}")

    print("\n=== 邻接表表示法 ===")
    adj_list = AdjacencyList()
    # 用人名作为节点，更直观
    adj_list.add_undirected_edge("小明", "小红")
    adj_list.add_undirected_edge("小明", "小刚")
    adj_list.add_undirected_edge("小红", "小刚")
    adj_list.add_undirected_edge("小红", "小丽")
    adj_list.add_undirected_edge("小刚", "小丽")
    adj_list.add_undirected_edge("小丽", "小王")
    adj_list.display()

    print(f"\n查询: 小明和小红是否相连? {adj_list.has_edge('小明', '小红')}")
    print(f"小明的朋友: {adj_list.get_neighbors('小明')}")

    print("\n=== 两种方式对比 ===")
    print("邻接矩阵: 查边O(1)，空间O(n²)，适合稠密图")
    print("邻接表:   查边O(邻居数)，空间O(n+m)，适合稀疏图")
    print("（n=节点数，m=边数）")

# 预期输出:
# === 邻接矩阵表示法 ===
#    v0  v1  v2  v3  v4
# v0  0  1  1  0  0
# v1  1  0  1  1  0
# v2  1  1  0  1  0
# v3  0  1  1  0  1
# v4  0  0  0  1  0
#
# 查询: 小明(0)和小红(1)是否相连? True
# 查询: 小明(0)和小王(4)是否相连? False
# 小明(0)的朋友: [(1, 1), (2, 1)]
#
# === 邻接表表示法 ===
#   小刚 -> (小明, w=1), (小红, w=1), (小丽, w=1)
#   小明 -> (小红, w=1), (小刚, w=1)
#   小红 -> (小明, w=1), (小刚, w=1), (小丽, w=1)
#   小丽 -> (小红, w=1), (小刚, w=1), (小王, w=1)
#   小王 -> (小丽, w=1)
#
# 查询: 小明和小红是否相连? True
# 小明的朋友: [('小红', 1), ('小刚', 1)]
#
# === 两种方式对比 ===
# 邻接矩阵: 查边O(1)，空间O(n²)，适合稠密图
# 邻接表:   查边O(邻居数)，空间O(n+m)，适合稀疏图
# （n=节点数，m=边数）
