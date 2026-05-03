# 挑战2：NP-completeness证明 ⭐⭐⭐

## 问题描述

证明**独立集问题**（Independent Set Problem）是NP-complete的。

独立集问题的定义：给定无向图G=(V,E)和整数k，是否存在大小至少为k的独立集？（独立集是指图中任意两个顶点都不相邻的顶点子集）

你需要完成以下步骤：
1. 证明独立集问题属于NP类
2. 通过多项式时间归约证明它是NP-hard的
3. 实现归约算法并验证其正确性

## 归约策略

使用**从顶点覆盖到独立集的归约**：

- **已知**：顶点覆盖问题是NP-complete的
- **目标**：证明独立集问题是NP-complete的
- **关键观察**：在任何图中，S是独立集当且仅当V-S是顶点覆盖

## 输入/输出规格

### 归约函数
```python
def vertex_cover_to_independent_set(vc_instance):
    """
    将顶点覆盖实例归约到独立集实例
    
    Args:
        vc_instance (tuple): (图, k) 其中图是邻接表，k是顶点覆盖大小上限
        
    Returns:
        tuple: (图, k') 对应的独立集实例，其中k' = |V| - k
    """
    pass
```

### 验证函数
```python
def verify_independent_set(graph, independent_set, k):
    """
    验证独立集解的正确性
    
    Args:
        graph (dict): 图的邻接表
        independent_set (set): 候选独立集
        k (int): 独立集大小下限
        
    Returns:
        bool: 如果是有效独立集且大小≥k返回True
    """
    pass
```

## 约束条件

- 归约必须是多项式时间的
- 归约必须保持等价性：原顶点覆盖实例有解当且仅当归约后的独立集实例有解
- 必须提供完整的数学证明（在代码注释中）
- 验证函数必须正确检查独立集的性质

## 提示

1. **互补性**：利用顶点覆盖和独立集的互补关系
2. **大小转换**：如果顶点覆盖大小≤k，则独立集大小≥|V|-k
3. **证明结构**：
   - 独立集 ∈ NP：给定候选解可以在多项式时间内验证
   - 独立集是NP-hard：通过从已知NP-complete问题（顶点覆盖）的归约
4. **边界情况**：考虑空图、完全图等特殊情况

<details>
<summary>参考解决方案</summary>

```python
def vertex_cover_to_independent_set(vc_instance):
    """
    从顶点覆盖到独立集的多项式时间归约
    
    数学证明：
    设G=(V,E)为无向图，S⊆V。
    
    引理：S是G的独立集 ⇔ V\S是G的顶点覆盖。
    
    证明：
    (⇒) 假设S是独立集。对于任意边(u,v)∈E，u和v不能同时在S中（否则违反独立集定义）。
         因此，至少有一个端点在V\S中，所以V\S是顶点覆盖。
    
    (⇐) 假设V\S是顶点覆盖。对于任意边(u,v)∈E，至少有一个端点在V\S中。
         因此，u和v不能同时在S中，所以S是独立集。
    
    因此，G有大小≤k的顶点覆盖 ⇔ G有大小≥|V|-k的独立集。
    
    归约：将顶点覆盖实例(G,k)映射到独立集实例(G, |V|-k)
    """
    graph, k = vc_instance
    num_vertices = len(graph)
    k_independent = num_vertices - k
    
    print(f"归约: 顶点覆盖(G, {k}) → 独立集(G, {k_independent})")
    return graph, k_independent

def verify_independent_set(graph, independent_set, k):
    """
    验证独立集解的正确性
    """
    print(f"验证独立集: {sorted(independent_set)}, k={k}")
    
    # 检查大小约束
    if len(independent_set) < k:
        print(f"  ✗ 大小不足: {len(independent_set)} < {k}")
        return False
    
    # 检查独立性：任意两点不相邻
    vertices_list = sorted(independent_set)
    for i in range(len(vertices_list)):
        for j in range(i + 1, len(vertices_list)):
            u, v = vertices_list[i], vertices_list[j]
            if v in graph.get(u, []):
                print(f"  ✗ 发现相邻顶点: ({u}, {v})")
                return False
    
    print("  ✓ 是有效的独立集")
    return True

def demonstrate_reduction():
    """演示归约过程"""
    # 示例图
    graph = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2, 4],
        4: [3]
    }
    
    print("原始图:")
    for node in sorted(graph):
        print(f"  {node}: {sorted(graph[node])}")
    
    # 顶点覆盖实例: k=2
    vc_instance = (graph, 2)
    print(f"\n顶点覆盖实例: k={2}")
    
    # 执行归约
    is_instance = vertex_cover_to_independent_set(vc_instance)
    graph_is, k_is = is_instance
    print(f"独立集实例: k={k_is}")
    
    # 测试解
    # 已知顶点覆盖 {1, 3} 是有效的
    vc_solution = {1, 3}
    is_solution = set(graph.keys()) - vc_solution  # 互补集
    print(f"\n对应的独立集解: {sorted(is_solution)}")
    
    result = verify_independent_set(graph_is, is_solution, k_is)
    print(f"验证结果: {'有效' if result else '无效'}")

if __name__ == "__main__":
    demonstrate_reduction()
```

</details>