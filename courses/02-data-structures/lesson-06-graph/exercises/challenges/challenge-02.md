# 挑战2：社交网络中的"六度分隔"验证

### 难度
⭐⭐⭐

### 描述
给定一个社交网络（无向图），验证"六度分隔"理论：从某个指定的人出发，计算到达网络中所有人的最短距离（好友链长度）。统计有多少人在6度以内、多少人不可达。

### 输入
- `graph`: 邻接表表示的无向图，key是人名（字符串），value是好友列表
- `start_person`: 起始人的名字

### 输出
一个字典，包含以下信息：
- `reachable`: 可到达的人数
- `within_6_degrees`: 6度以内可到达的人数（包括自己）
- `beyond_6_degrees`: 超过6度才能到达的人数
- `unreachable`: 无法到达的人数
- `max_degree`: 最大分隔度数
- `average_degree`: 平均分隔度数（只算可达的，保留2位小数）

### 示例

**示例 1:**
```
输入:
graph = {
    "小明": ["小红", "小刚"],
    "小红": ["小明", "小刚", "小丽"],
    "小刚": ["小明", "小红", "小王"],
    "小丽": ["小红", "小李"],
    "小王": ["小刚"],
    "小李": ["小丽"]
}
start_person = "小明"

输出:
{
    "reachable": 5,
    "within_6_degrees": 6,
    "beyond_6_degrees": 0,
    "unreachable": 0,
    "max_degree": 3,
    "average_degree": 1.60
}

解释:
小明到小红: 1度, 小刚: 1度, 小丽: 2度(小明→小红→小丽)
小王: 2度(小明→小刚→小王), 小李: 3度(小明→小红→小丽→小李)
所有人都在6度以内！
```

### 约束条件
- 图中人数：1 ≤ n ≤ 1000
- 每个人至少有一个好友或为孤立节点
- start_person 一定在图中
- 图可能不连通

### 提示
- BFS天然适合找无权图的最短路径
- 记录每个节点的距离，BFS一层一层扩散
- 注意处理不连通的情况（不可达的人标记为不可达）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
这是BFS的直接应用。从start_person出发做BFS，记录每个节点被访问时的距离。然后统计各距离区间的人数。

### 代码

```python
from collections import deque


def six_degrees_analysis(graph, start_person):
    """
    验证社交网络中的六度分隔理论
    参数: graph - 社交网络邻接表, start_person - 起始人
    返回: 包含各项统计信息的字典
    """
    if start_person not in graph:
        return {"error": "起始人不在图中"}

    # BFS计算最短距离
    distances = {start_person: 0}
    queue = deque([start_person])

    while queue:
        current = queue.popleft()
        for friend in graph.get(current, []):
            if friend not in distances:
                distances[friend] = distances[current] + 1
                queue.append(friend)

    # 统计
    total_people = len(graph) - 1  # 不包括自己
    reachable = len(distances) - 1  # 不包括自己
    unreachable = total_people - reachable

    within_6 = 0  # 6度以内（不包括自己，0度）
    beyond_6 = 0

    for person, dist in distances.items():
        if person == start_person:
            continue  # 跳过自己
        if dist <= 6:
            within_6 += 1
        else:
            beyond_6 += 1

    # 计算最大和平均度数（不包括自己）
    max_degree = 0
    total_dist = 0
    for person, dist in distances.items():
        if person == start_person:
            continue
        max_degree = max(max_degree, dist)
        total_dist += dist

    avg_degree = round(total_dist / reachable, 2) if reachable > 0 else 0

    return {
        "reachable": reachable,
        "within_6_degrees": within_6,
        "beyond_6_degrees": beyond_6,
        "unreachable": unreachable,
        "max_degree": max_degree,
        "average_degree": avg_degree
    }


# ===== 测试 =====
if __name__ == "__main__":
    social_graph = {
        "小明": ["小红", "小刚"],
        "小红": ["小明", "小刚", "小丽"],
        "小刚": ["小明", "小红", "小王"],
        "小丽": ["小红", "小李"],
        "小王": ["小刚"],
        "小李": ["小丽"]
    }

    result = six_degrees_analysis(social_graph, "小明")
    print(f"可达人数: {result['reachable']}")
    print(f"6度以内: {result['within_6_degrees']}")
    print(f"超过6度: {result['beyond_6_degrees']}")
    print(f"不可达: {result['unreachable']}")
    print(f"最大分隔度: {result['max_degree']}")
    print(f"平均分隔度: {result['average_degree']}")

# 预期输出:
# 可达人数: 5
# 6度以内: 5
# 超过6度: 0
# 不可达: 0
# 最大分隔度: 3
# 平均分隔度: 1.6
```

### 复杂度分析
- 时间复杂度: O(V+E)，BFS遍历整个连通分量
- 空间复杂度: O(V)，distances字典和队列最多存储V个节点

</details>
