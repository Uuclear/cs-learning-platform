# 挑战1：找出图中的所有连通分量

### 难度
⭐⭐

### 描述
给定一个无向图（用邻接表表示），找出图中所有的连通分量。每个连通分量是一个节点列表，返回所有连通分量的列表。

**连通分量**的定义：一个连通分量是图中一个最大的子图，其中任意两个节点之间都有路径可达。

### 输入
一个字典，key是节点（整数），value是邻居列表（整数列表）。

```python
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [4],
    4: [3],
    5: []
}
```

### 输出
一个列表，每个元素是一个连通分量的节点列表。

```python
[[0, 1, 2], [3, 4], [5]]
```

### 示例

**示例 1:**
```
输入: {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3], 5: []}
输出: [[0, 1, 2], [3, 4], [5]]
解释: 图中有3个连通分量：{0,1,2}互相连接，{3,4}互相连接，{5}是孤立节点
```

**示例 2:**
```
输入: {0: [1], 1: [0]}
输出: [[0, 1]]
解释: 只有一个连通分量
```

### 约束条件
- 节点数：0 ≤ n ≤ 100
- 图是无向的
- 邻接表中每个节点的邻居列表可能为空（孤立节点）
- 孤立节点也算一个连通分量（大小为1）

### 提示
- 对每个未访问的节点启动一次BFS或DFS
- 每次BFS/DFS能访问到的所有节点就是一个连通分量
- 遍历完所有节点后，你就找到了所有连通分量

### 进阶思考
- 如果图有100万个节点，你的算法还能高效运行吗？
- BFS和DFS在这个问题中哪个更合适？为什么？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
核心思想很简单：**对每个还没访问过的节点启动一次BFS，这次BFS能访问到的所有节点就是一个连通分量**。重复这个过程，直到所有节点都被访问。

这就像你有一张纸上有几堆互相连接的点，你用笔从某个点开始涂色，所有能连通的点都被涂上同一个颜色。然后换一个没涂色的点，用新颜色涂，以此类推。最后每种颜色就是一个连通分量。

### 代码

```python
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
```

### 复杂度分析
- 时间复杂度: O(V+E)，每个节点和每条边都只访问一次
- 空间复杂度: O(V)，visited集合和队列最多存储V个节点

</details>
