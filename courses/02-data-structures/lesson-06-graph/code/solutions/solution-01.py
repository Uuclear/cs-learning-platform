# 解答1：找出图中的所有连通分量

from collections import deque


def find_connected_components(graph):
    """
    找出无向图的所有连通分量
    参数: graph - 邻接表，key是节点，value是邻居列表
    返回: 连通分量列表，每个分量是一个节点列表
    """
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            # 每次BFS找到一个新连通分量
            component = []
            queue = deque([node])
            visited.add(node)

            while queue:
                current = queue.popleft()
                component.append(current)

                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(sorted(component))  # 排序方便对比

    return components


# ===== 测试 =====
if __name__ == "__main__":
    graph1 = {
        0: [1, 2],
        1: [0, 2],
        2: [0, 1],
        3: [4],
        4: [3],
        5: []
    }
    print(f"测试1: {find_connected_components(graph1)}")
    # 输出: [[0, 1, 2], [3, 4], [5]]

    graph2 = {0: [1], 1: [0]}
    print(f"测试2: {find_connected_components(graph2)}")
    # 输出: [[0, 1]]

    graph3 = {}
    print(f"测试3: {find_connected_components(graph3)}")
    # 输出: []
