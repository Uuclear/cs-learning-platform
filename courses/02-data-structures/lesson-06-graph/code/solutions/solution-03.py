# 解答3：加权图中的最短配送路线

import heapq


def dijkstra(graph, start):
    """
    Dijkstra最短路径算法
    参数: graph - 加权有向图邻接表, start - 起点
    返回: (最短距离字典, 前驱节点字典)
    """
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
    """
    根据前驱节点回溯最短路径
    返回: 路径列表，如果不可达返回None
    """
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
