# 编程挑战2：城市道路重建规划

## 背景
一个城市需要重建其道路网络，目标是以最低成本连接所有区域。城市规划部门提供了现有的道路连接图和每条道路的重建成本。

然而，有些区域之间可能存在多条可选道路，你需要选择最优的道路组合来最小化总成本。

## 任务
实现一个函数 `plan_road_reconstruction(areas: List[str], roads: List[Tuple[str, str, int]]) -> Tuple[int, List[Tuple[str, str]]]`，该函数使用最小生成树算法规划道路重建。

## 要求
- 输入：
  - `areas`: 所有区域的名称列表
  - `roads`: 可选道路列表，每个元素为 `(区域1, 区域2, 成本)`
- 输出：
  - 元组 `(总成本, 选中的道路列表)`
  - 如果无法连接所有区域，返回 `(-1, [])`
- 道路是双向的（无向图）

## 示例
```python
areas = ['A', 'B', 'C', 'D']
roads = [
    ('A', 'B', 4),
    ('A', 'C', 1),
    ('A', 'D', 2),
    ('B', 'D', 3),
    ('C', 'D', 5)
]

total_cost, selected_roads = plan_road_reconstruction(areas, roads)
# total_cost 应该是 6
# selected_roads 应该是 [('A', 'C'), ('A', 'D'), ('B', 'D')]
```

## 提示
- 你可以选择实现Prim算法或Kruskal算法
- 对于Kruskal算法，你可能需要实现并查集数据结构
- 确保处理图不连通的情况
- 注意道路是无向的，所以在构建图时要双向添加