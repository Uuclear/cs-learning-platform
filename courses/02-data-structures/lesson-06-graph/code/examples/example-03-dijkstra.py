# 最短路径算法：Dijkstra（迪杰斯特拉）
# 就像导航App：不只是看"几步到"，还要看"每步多远"
# BFS说"经过的节点最少"，Dijkstra说"走的总路程最短"

import heapq


class WeightedGraph:
    """加权图，用邻接表+优先队列实现Dijkstra"""

    def __init__(self):
        self.graph = {}

    def add_edge(self, src, dst, weight):
        """添加有向边和权重"""
        if src not in self.graph:
            self.graph[src] = []
        if dst not in self.graph:
            self.graph[dst] = []
        self.graph[src].append((dst, weight))

    def add_undirected_edge(self, v1, v2, weight):
        """添加无向边"""
        self.add_edge(v1, v2, weight)
        self.add_edge(v2, v1, weight)

    def dijkstra(self, start):
        """
        Dijkstra算法：找到从起点到所有其他节点的最短路径
        核心思想：贪心 + 优先队列
        每次选"当前已知最近的未处理节点"，然后更新它的邻居

        时间复杂度：O((V+E) log V)，V是节点数，E是边数
        """
        # 初始化：所有节点的距离设为无穷大
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0  # 起点到自己的距离是0

        # 记录最短路径的前驱节点（用于回溯路径）
        previous = {vertex: None for vertex in self.graph}

        # 优先队列：(距离, 节点)
        # heapq保证每次弹出的是距离最小的
        pq = [(0, start)]

        while pq:
            current_dist, current_vertex = heapq.heappop(pq)

            # 如果已经找到了更短的路径到这个节点，跳过
            if current_dist > distances[current_vertex]:
                continue

            # 遍历当前节点的所有邻居
            for neighbor, weight in self.graph.get(current_vertex, []):
                distance = current_dist + weight

                # 如果找到了一条更短的路，更新它
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous

    def get_shortest_path(self, start, end):
        """获取从起点到终点的最短路径和距离"""
        distances, previous = self.dijkstra(start)

        # 回溯路径
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        # 如果起点到终点不可达
        if distances[end] == float('infinity'):
            return None, float('infinity')

        return path, distances[end]

    def display(self):
        """打印图的结构"""
        for vertex in sorted(self.graph.keys()):
            edges = self.graph[vertex]
            edge_str = ", ".join(f"{n}(距离{w})" for n, w in edges)
            print(f"  {vertex} -> {edge_str}")


# ===== 测试 =====
if __name__ == "__main__":
    # 用城市之间的公路距离来演示
    #
    #        北京
    #       /    \
    #   200       500
    #     /        \
    #   天津 --- 350 --- 济南
    #     |             |
    #   150           400
    #     |             |
    #   青岛 --- 300 --- 南京
    #       \         /
    #       250     200
    #         \     /
    #          上海
    #

    g = WeightedGraph()
    # 城市之间的公路距离（公里）
    g.add_undirected_edge("北京", "天津", 120)
    g.add_undirected_edge("北京", "济南", 400)
    g.add_undirected_edge("天津", "济南", 300)
    g.add_undirected_edge("天津", "青岛", 350)
    g.add_undirected_edge("济南", "南京", 600)
    g.add_undirected_edge("青岛", "南京", 450)
    g.add_undirected_edge("青岛", "上海", 700)
    g.add_undirected_edge("南京", "上海", 300)

    print("=== 城市之间的公路网络 ===")
    g.display()

    print("\n=== Dijkstra：从北京到所有城市的最短距离 ===")
    distances, previous = g.dijkstra("北京")
    print("从北京出发：")
    for city in sorted(distances.keys()):
        if city != "北京":
            print(f"  到 {city}: {distances[city]} 公里")

    print("\n=== 最短路径：北京 -> 上海 ===")
    path, dist = g.get_shortest_path("北京", "上海")
    if path:
        print(f"最短路径: {' -> '.join(path)}")
        print(f"总距离: {dist} 公里")
    else:
        print("不可达！")

    print("\n=== 最短路径：北京 -> 南京 ===")
    path2, dist2 = g.get_shortest_path("北京", "南京")
    if path2:
        print(f"最短路径: {' -> '.join(path2)}")
        print(f"总距离: {dist2} 公里")

    print("\n=== Dijkstra 注意事项 ===")
    print("1. Dijkstra不能处理负权边（负距离没意义，但负权重的图要用Bellman-Ford）")
    print("2. 如果所有边权重相同，Dijkstra退化成了BFS")
    print("3. Dijkstra是贪心算法：每次都选当前最近的，全局最优")

# 预期输出:
# === 城市之间的公路网络 ===
#   北京 -> 天津(距离120), 济南(距离400)
#   天津 -> 北京(距离120), 济南(距离300), 青岛(距离350)
#   济南 -> 北京(距离400), 天津(距离300), 南京(距离600)
#   南京 -> 济南(距离600), 青岛(距离450), 上海(距离300)
#   上海 -> 青岛(距离700), 南京(距离300)
#   青岛 -> 天津(距离350), 南京(距离450), 上海(距离700)
#
# === Dijkstra：从北京到所有城市的最短距离 ===
# 从北京出发：
#   到 上海: 1170 公里
#   到 南京: 920 公里
#   到 天津: 120 公里
#   到 济南: 400 公里
#   到 青岛: 470 公里
#
# === 最短路径：北京 -> 上海 ===
# 最短路径: 北京 -> 天津 -> 青岛 -> 上海
# 总距离: 1170 公里
#
# === 最短路径：北京 -> 南京 ===
# 最短路径: 北京 -> 天津 -> 青岛 -> 南京
# 总距离: 920 公里
#
# === Dijkstra 注意事项 ===
# 1. Dijkstra不能处理负权边（负距离没意义，但负权重的图要用Bellman-Ford）
# 2. 如果所有边权重相同，Dijkstra退化成了BFS
# 3. Dijkstra是贪心算法：每次都选当前最近的，全局最优
