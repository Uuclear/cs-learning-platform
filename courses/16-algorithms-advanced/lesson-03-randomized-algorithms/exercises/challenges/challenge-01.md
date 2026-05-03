# 挑战1：随机选择算法实现 ⭐⭐

## 问题描述

实现**随机选择算法**（Randomized Selection），也称为Quickselect，用于在未排序数组中找到第k小的元素。

随机选择算法是快速排序的变种，但它只递归处理包含目标元素的一侧，因此期望时间复杂度为O(n)。

## 输入/输出规格

### 函数定义
```python
def randomized_select(arr, k):
    """
    在数组中找到第k小的元素（k从0开始）
    
    Args:
        arr (list): 输入数组
        k (int): 要找的第k小元素的索引（0 <= k < len(arr)）
        
    Returns:
        tuple: (第k小的元素, 性能统计字典)
    """
    pass
```

### 示例
```python
arr = [3, 1, 4, 1, 5, 9, 2, 6]
result, stats = randomized_select(arr, 3)  # 找第4小的元素（索引3）
print(result)  # 输出: 3
print(stats)   # 包含比较次数、交换次数等信息
```

## 约束条件

- 必须使用随机主元选择策略
- 时间复杂度期望为O(n)，最坏情况为O(n²)
- 空间复杂度为O(1)（原地操作）
- 必须正确处理重复元素和边界情况
- 需要返回详细的性能统计信息

## 提示

1. **分区策略**：使用与随机快速排序相同的分区函数
2. **递归优化**：只递归处理包含第k小元素的那一侧
3. **性能跟踪**：记录比较次数、交换次数、递归深度
4. **边界处理**：注意k的有效范围检查和空数组处理

<details>
<summary>参考解决方案</summary>

```python
import random

class RandomizedSelect:
    """
    随机选择算法实现
    """
    
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.recursion_depth = 0
        self.max_depth = 0
    
    def _partition(self, arr, low, high):
        """随机分区函数"""
        # 随机选择主元
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        self.swaps += 1
        
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.swaps += 1
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if i + 1 != high:
            self.swaps += 1
        
        return i + 1
    
    def _select_recursive(self, arr, low, high, k, depth=0):
        """递归选择函数"""
        self.recursion_depth = depth
        self.max_depth = max(self.max_depth, depth)
        
        if low == high:
            return arr[low]
        
        # 分区
        pivot_index = self._partition(arr, low, high)
        
        # 计算主元的位置（相对于low）
        pivot_rank = pivot_index - low
        
        if k == pivot_rank:
            return arr[pivot_index]
        elif k < pivot_rank:
            return self._select_recursive(arr, low, pivot_index - 1, k, depth + 1)
        else:
            return self._select_recursive(arr, pivot_index + 1, high, k - pivot_rank - 1, depth + 1)
    
    def select(self, arr, k):
        """主选择函数"""
        if not arr:
            raise ValueError("数组为空")
        if k < 0 or k >= len(arr):
            raise ValueError(f"k必须在[0, {len(arr)-1}]范围内")
        
        # 重置计数器
        self.comparisons = 0
        self.swaps = 0
        self.max_depth = 0
        
        # 创建数组副本以避免修改原数组
        arr_copy = arr.copy()
        result = self._select_recursive(arr_copy, 0, len(arr_copy) - 1, k)
        
        return result, {
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'max_depth': self.max_depth,
            'array_size': len(arr)
        }

def randomized_select(arr, k):
    """便捷函数接口"""
    selector = RandomizedSelect()
    return selector.select(arr, k)

# 测试和分析
def test_randomized_select():
    """测试随机选择算法"""
    print("=== 随机选择算法测试 ===")
    
    test_cases = [
        ([3, 1, 4, 1, 5, 9, 2, 6], 3),
        ([1, 2, 3, 4, 5], 0),
        ([5, 4, 3, 2, 1], 4),
        ([7], 0),
        ([2, 2, 2, 2], 2)
    ]
    
    for arr, k in test_cases:
        result, stats = randomized_select(arr, k)
        expected = sorted(arr)[k]
        correct = result == expected
        
        print(f"数组: {arr}, k={k}")
        print(f"结果: {result}, 期望: {expected}, 正确: {correct}")
        print(f"统计: 比较={stats['comparisons']}, 交换={stats['swaps']}, 深度={stats['max_depth']}")
        print()

if __name__ == "__main__":
    test_randomized_select()
```

</details>