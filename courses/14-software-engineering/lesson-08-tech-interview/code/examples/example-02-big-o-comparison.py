# 示例2：不同算法复杂度的比较与可视化
import time
import random
from typing import List, Callable

def linear_search(arr: List[int], target: int) -> int:
    """线性搜索 - O(n)"""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def bubble_sort(arr: List[int]) -> List[int]:
    """冒泡排序 - O(n²)"""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def merge_sort(arr: List[int]) -> List[int]:
    """归并排序 - O(n log n)"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """归并两个已排序数组"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def time_algorithm(algorithm: Callable, data: List[int], *args) -> float:
    """测量算法执行时间"""
    start_time = time.time()
    algorithm(data, *args) if args else algorithm(data)
    end_time = time.time()
    return end_time - start_time

def compare_complexities():
    """比较不同算法的时间复杂度"""
    sizes = [100, 500, 1000, 2000]
    linear_times = []
    quadratic_times = []
    nlogn_times = []

    for size in sizes:
        # 生成随机数据
        data = [random.randint(1, 1000) for _ in range(size)]
        target = random.choice(data)

        # 测试线性搜索
        linear_time = time_algorithm(linear_search, data, target)
        linear_times.append(linear_time)

        # 测试冒泡排序（仅小数据集）
        if size <= 1000:
            quadratic_time = time_algorithm(bubble_sort, data)
            quadratic_times.append(quadratic_time)
        else:
            quadratic_times.append(0)  # 跳过大数组的冒泡排序

        # 测试归并排序
        nlogn_time = time_algorithm(merge_sort, data)
        nlogn_times.append(nlogn_time)

    print("算法复杂度比较结果:")
    print("数据规模\t线性搜索(O(n))\t冒泡排序(O(n²))\t归并排序(O(n log n))")
    for i, size in enumerate(sizes):
        quad_time = f"{quadratic_times[i]:.4f}" if quadratic_times[i] > 0 else "跳过"
        print(f"{size}\t\t{linear_times[i]:.4f}\t\t{quad_time}\t\t{nlogn_times[i]:.4f}")

if __name__ == "__main__":
    compare_complexities()
    print("\n注意: 实际面试中应优先选择高效算法!")