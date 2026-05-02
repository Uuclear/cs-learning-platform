# 挑战3：加权图中的最短配送路线

### 难度
⭐⭐⭐⭐

### 描述
你是一家外卖公司的调度系统。给定一组餐厅和顾客的加权有向图，你需要：

1. 找到从配送中心到所有餐厅的最短距离
2. 从某个餐厅取餐后，找到到达所有顾客的最短路径
3. 计算总配送时间（配送中心→餐厅→顾客的总时间最短）

### 输入
- `graph`: 加权有向图的邻接表，key是地点名（字符串），value是(目的地, 时间分钟)的列表
- `hub`: 配送中心的位置
- `restaurants`: 餐厅位置列表
- `customers`: 顾客位置列表

### 输出
对于每个顾客，输出最优的配送路线（经过哪个餐厅）和总时间：
- `customer`: 顾客名
- `route`: 配送路线（配送中心→餐厅→顾客）
- `total_time`: 总配送时间（分钟）

### 示例

**示例 1:**
```
输入:
graph = {
    "配送中心": [("餐厅A", 10), ("餐厅B", 15), ("餐厅C", 25)],
    "餐厅A": [("顾客1", 20), ("顾客2", 30)],
    "餐厅B": [("顾客1", 10), ("顾客3", 15)],
    "餐厅C": [("顾客2", 10), ("顾客3", 20)],
    "顾客1": [],
    "顾客2": [],
    "顾客3": []
}
hub = "配送中心"
restaurants = ["餐厅A", "餐厅B", "餐厅C"]
customers = ["顾客1", "顾客2", "顾客3"]

输出:
[
    {"customer": "顾客1", "route": ["配送中心", "餐厅B", "顾客1"], "total_time": 25},
    {"customer": "顾客2", "route": ["配送中心", "餐厅A", "顾客2"], "total_time": 40},
    {"customer": "顾客3", "route": ["配送中心", "餐厅B", "顾客3"], "total_time": 30}
]
```

### 约束条件
- 图中节点数：3 ≤ n ≤ 100
- 边权均为正数（配送时间不可能为负）
- 每个顾客至少可以通过一个餐厅从配送中心到达
- 配送路线必须是：配送中心 → 某个餐厅 → 顾客（中间可能有其他节点）

### 提示
- 首先用Dijkstra从配送中心找到到所有餐厅的最短距离
- 然后从每个餐厅用Dijkstra找到到所有顾客的最短距离
- 对于每个顾客，选择"配送中心到餐厅 + 餐厅到顾客"总时间最短的餐厅

### 进阶思考
- 如果一个骑手可以同时送多单，怎么优化调度？
- 如果餐厅有"出餐等待时间"，怎么把它纳入模型？
- 如果顾客有"最晚送达时间"要求，怎么判断能否满足？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
分三步：
1. 用Dijkstra计算配送中心到所有节点的最短距离
2. 对每个餐厅，用Dijkstra计算到所有顾客的最短距离
3. 对每个顾客，遍历所有餐厅，找到"hub到餐厅 + 餐厅到顾客"总时间最短的组合

### 代码

```python
import heapq


def dijkstra(graph, start):
    """Dijkstra最短路径算法"""
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        dist, current = heapq.heappop(pq)
        if dist > distances[current]:
            continue
        for neighbor, weight in graph.get(current, []):
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, previous


def get_path(previous, start, end):
    """回溯最短路径"""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    if path[0] != start:
        return None  # 不可达
    return path


def optimize_delivery(graph, hub, restaurants, customers):
    """
    优化外卖配送路线
    参数: graph-加权有向图, hub-配送中心,
         restaurants-餐厅列表, customers-顾客列表
    返回: 每个顾客的最优配送方案列表
    """
    # 第1步：配送中心到所有节点的最短距离
    hub_distances, hub_previous = dijkstra(graph, hub)

    results = []

    for customer in customers:
        best_total = float('infinity')
        best_route = None
        best_restaurant = None

        for restaurant in restaurants:
            # 餐厅到顾客的最短距离
            rest_distances, rest_previous = dijkstra(graph, restaurant)

            # 总时间 = hub到餐厅 + 餐厅到顾客
            hub_to_rest = hub_distances[restaurant]
            rest_to_customer = rest_distances[customer]
            total = hub_to_rest + rest_to_customer

            if total < best_total:
                best_total = total
                best_restaurant = restaurant

                # 构造完整路径
                path1 = get_path(hub_previous, hub, restaurant)
                path2 = get_path(rest_previous, restaurant, customer)
                if path1 and path2:
                    # 拼接路径（餐厅只出现一次）
                    best_route = path1[:-1] + path2

        if best_route:
            results.append({
                "customer": customer,
                "route": best_route,
                "total_time": best_total
            })
        else:
            results.append({
                "customer": customer,
                "route": None,
                "total_time": -1
            })

    return results


# ===== 测试 =====
if __name__ == "__main__":
    delivery_graph = {
        "配送中心": [("餐厅A", 10), ("餐厅B", 15), ("餐厅C", 25)],
        "餐厅A": [("顾客1", 20), ("顾客2", 30)],
        "餐厅B": [("顾客1", 10), ("顾客3", 15)],
        "餐厅C": [("顾客2", 10), ("顾客3", 20)],
        "顾客1": [],
        "顾客2": [],
        "顾客3": []
    }

    hub = "配送中心"
    restaurants = ["餐厅A", "餐厅B", "餐厅C"]
    customers = ["顾客1", "顾客2", "顾客3"]

    results = optimize_delivery(delivery_graph, hub, restaurants, customers)
    for r in results:
        print(f"{r['customer']}: {' → '.join(r['route'])} (用时{r['total_time']}分钟)")

# 预期输出:
# 顾客1: 配送中心 → 餐厅B → 顾客1 (用时25分钟)
# 顾客2: 配送中心 → 餐厅A → 顾客2 (用时40分钟)
# 顾客3: 配送中心 → 餐厅B → 顾客3 (用时30分钟)
```

### 复杂度分析
- 时间复杂度: O(R × (V+E) log V)，R是餐厅数，每次Dijkstra是O((V+E) log V)
- 空间复杂度: O(V)，存储距离和前驱节点

</details>
