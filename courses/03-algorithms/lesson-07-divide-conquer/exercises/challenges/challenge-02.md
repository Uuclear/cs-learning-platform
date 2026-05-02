# 编程挑战2：二维平面最近点对优化 ⭐⭐⭐

## 问题描述

在之前的最近点对示例中，我们实现了一个 O(n log n) 的分治算法。现在需要进一步优化这个算法，使其在实际运行中更快。

具体来说，需要优化 strip 中的比较过程。理论上我们只需要比较每个点与其后最多7个点，但实际上可以进一步减少比较次数。

## 要求

- 实现一个优化版本的最近点对算法
- 在 strip 处理阶段，使用更高效的策略减少不必要的距离计算
- 确保算法正确性不变
- 分析优化后的实际性能提升

## 提示

1. 可以考虑使用更精确的几何性质来限制需要比较的点的数量
2. 或者使用预处理步骤来进一步筛选候选点
3. 注意保持算法的时间复杂度仍然是 O(n log n)

## 测试用例

使用随机生成的大规模点集进行测试，比较优化前后的时间差异：

```python
import random
import time

# 生成1000个随机点
points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(1000)]

# 测试原始算法
start = time.time()
result1 = closest_pair_original(points)
time1 = time.time() - start

# 测试优化算法  
start = time.time()
result2 = closest_pair_optimized(points)
time2 = time.time() - start

# 验证结果相同
assert abs(result1[2] - result2[2]) < 1e-10
print(f"原始算法时间: {time1:.4f}s")
print(f"优化算法时间: {time2:.4f}s")
print(f"性能提升: {(time1/time2):.2f}x")
```