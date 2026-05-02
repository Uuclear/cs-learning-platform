# 挑战3：K个有序数组的合并

## 难度
⭐⭐⭐⭐

## 描述
给定 **K 个已经从小到大排序好的数组**，请将它们合并成一个大的有序数组。要求使用类似归并排序中 `merge` 的思想，但不能简单地先把所有元素拼起来再排序。

## 输入
一个包含 K 个有序数组的列表，例如 `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`

## 输出
合并后的有序数组

## 示例

**示例 1:**
```
输入: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
输出: [1, 2, 3, 4, 5, 6, 7, 8, 9]
解释: 三个有序数组合并后得到一个完整有序数组
```

**示例 2:**
```
输入: [[1, 3], [2], [4, 5, 6]]
输出: [1, 2, 3, 4, 5, 6]
解释: 数组长度可以不同
```

**示例 3:**
```
输入: []
输出: []
解释: 空输入返回空数组
```

## 约束条件
- K >= 0（数组个数可以为0）
- 每个子数组的长度 >= 0
- 每个子数组内部已经从小到大排序
- 总元素数不超过 100,000

## 提示
- 简单方法：每次从 K 个数组的当前元素中选最小的放入结果（O(K) 每次选择）
- 进阶方法：使用最小堆（优先队列）来优化选择过程，将每次选择的时间从 O(K) 降到 O(log K)
- 先实现简单方法，再尝试用 Python 的 `heapq` 模块实现进阶方法

## 进阶思考
- 简单方法的时间复杂度是多少？
- 使用堆优化后的时间复杂度是多少？
- 如果 K 很大（比如 10000），两种方法的差距有多大？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
使用 K 个指针分别指向每个数组的当前位置，每次选择 K 个指针所指元素中最小的那个放入结果数组，然后将该指针向前移动一位。重复直到所有数组都处理完。

### 代码（简单方法）
```python
def merge_k_arrays(arrays):
    """
    合并K个有序数组（简单方法）
    参数: arrays - 包含K个有序数组的列表
    返回: 合并后的有序数组
    """
    k = len(arrays)
    # 初始化每个数组的指针
    pointers = [0] * k
    result = []

    # 计算总元素数
    total = sum(len(arr) for arr in arrays)

    for _ in range(total):
        min_val = float('inf')
        min_idx = -1

        # 从K个指针中找最小值
        for i in range(k):
            if pointers[i] < len(arrays[i]):
                if arrays[i][pointers[i]] < min_val:
                    min_val = arrays[i][pointers[i]]
                    min_idx = i

        # 将最小值放入结果，移动对应指针
        result.append(min_val)
        pointers[min_idx] += 1

    return result


# 测试
if __name__ == "__main__":
    test = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"输入: {test}")
    result = merge_k_arrays(test)
    print(f"输出: {result}")

# 输出:
# 输入: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
# 输出: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 代码（进阶方法：使用堆）
```python
import heapq

def merge_k_arrays_heap(arrays):
    """
    合并K个有序数组（使用最小堆优化）
    参数: arrays - 包含K个有序数组的列表
    返回: 合并后的有序数组
    """
    result = []
    # 初始化堆：放入每个数组的第一个元素
    # 堆中元素格式：(值, 数组索引, 元素在该数组中的索引)
    heap = []
    for i, arr in enumerate(arrays):
        if arr:  # 跳过空数组
            heapq.heappush(heap, (arr[0], i, 0))

    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # 如果该数组还有下一个元素，放入堆中
        next_idx = elem_idx + 1
        if next_idx < len(arrays[arr_idx]):
            heapq.heappush(heap, (arrays[arr_idx][next_idx], arr_idx, next_idx))

    return result


# 测试
if __name__ == "__main__":
    test = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"输入: {test}")
    result = merge_k_arrays_heap(test)
    print(f"输出: {result}")

# 输出:
# 输入: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
# 输出: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 复杂度分析
- 简单方法:
  - 时间复杂度: O(N × K)，其中 N 是总元素数，K 是数组个数。每次选最小需要遍历 K 个指针
  - 空间复杂度: O(N) 存储结果
- 堆优化方法:
  - 时间复杂度: O(N × log K)，堆的大小最多为 K，每次弹出和插入都是 O(log K)
  - 空间复杂度: O(N) 存储结果 + O(K) 存储堆

</details>
