# 挑战2：排序算法大比拼

## 难度
⭐⭐⭐

## 描述
请实现一个函数，对同一个输入数组分别使用**冒泡排序**、**插入排序**和**快速排序**，并统计每种算法的**比较次数**和**运行时间**。通过对比实验，验证 O(n log n) 算法相对于 O(n²) 算法的优势。

## 输入
随机生成的整数数组（建议长度 1000~10000）

## 输出
打印每种算法的名称、比较次数、运行时间（毫秒），格式如下：

```
算法名称        比较次数        运行时间(ms)
冒泡排序        XXXXX          XX.XX
插入排序        XXXXX          XX.XX
快速排序        XXXX           X.XX
```

## 示例

```
输入: 随机生成1000个整数的数组
输出:
算法名称        比较次数        运行时间(ms)
冒泡排序        500500         125.34
插入排序        250123         62.17
快速排序        10234          1.23
```

## 约束条件
- 数组长度：500 <= n <= 10000
- 每次排序前，使用数组的副本（不能修改原数组）
- 使用 `time` 模块测量运行时间

## 提示
- 用 `arr.copy()` 创建副本，避免修改原数据
- 在比较的地方增加计数器（如 `comparisons += 1`）
- 使用 `time.time()` 或 `time.perf_counter()` 测量时间
- 尝试不同大小的数组（1000、5000、10000），观察增长趋势

## 进阶思考
- 随着 n 的增大，三种算法的时间比是如何变化的？
- 插入排序的比较次数通常比冒泡排序少，为什么？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
为每种排序算法添加比较计数器，用 `time.perf_counter()` 测量运行时间。对同一个数组的副本分别排序，收集结果后打印对比表。

### 代码
```python
import time

def bubble_sort_with_count(arr):
    """冒泡排序（带计数）"""
    comparisons = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return comparisons


def insertion_sort_with_count(arr):
    """插入排序（带计数）"""
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return comparisons


def quick_sort_with_count(arr):
    """快速排序（带计数）"""
    comparisons = [0]  # 用列表存引用，方便在嵌套函数中修改

    def _quick_sort(a):
        if len(a) <= 1:
            return a
        pivot = a[len(a) // 2]
        left = []
        middle = []
        right = []
        for x in a:
            comparisons[0] += 1
            if x < pivot:
                left.append(x)
            elif x == pivot:
                middle.append(x)
            else:
                right.append(x)
        return _quick_sort(left) + middle + _quick_sort(right)

    _quick_sort(arr)
    return comparisons[0]


def compare_sorts(n=1000):
    """对比三种排序算法"""
    import random
    random.seed(42)  # 固定随机种子，保证可复现
    original = [random.randint(1, 10000) for _ in range(n)]

    results = []

    # 冒泡排序
    arr = original.copy()
    t0 = time.perf_counter()
    comps = bubble_sort_with_count(arr)
    t1 = time.perf_counter()
    results.append(("冒泡排序", comps, (t1 - t0) * 1000))

    # 插入排序
    arr = original.copy()
    t0 = time.perf_counter()
    comps = insertion_sort_with_count(arr)
    t1 = time.perf_counter()
    results.append(("插入排序", comps, (t1 - t0) * 1000))

    # 快速排序
    arr = original.copy()
    t0 = time.perf_counter()
    comps = quick_sort_with_count(arr)
    t1 = time.perf_counter()
    results.append(("快速排序", comps, (t1 - t0) * 1000))

    # 打印对比表
    print(f"数组长度: {n}")
    print(f"{'算法名称':<10} {'比较次数':<12} {'运行时间(ms)':<15}")
    print("-" * 40)
    for name, comps, elapsed in results:
        print(f"{name:<10} {comps:<12} {elapsed:<15.2f}")


if __name__ == "__main__":
    compare_sorts(1000)

# 输出（示例，具体数值取决于随机种子和数据）:
# 数组长度: 1000
# 算法名称     比较次数       运行时间(ms)
# ----------------------------------------
# 冒泡排序     500500       15.23
# 插入排序     251234       7.81
# 快速排序     10456        0.89
```

### 复杂度分析
- 冒泡排序: 时间复杂度 O(n²)，比较次数约 n(n-1)/2
- 插入排序: 时间复杂度 O(n²)，但实际比较次数通常少于冒泡
- 快速排序: 时间复杂度 O(n log n)，比较次数显著更少

</details>
