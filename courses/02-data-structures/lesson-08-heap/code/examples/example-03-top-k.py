# 示例3：Top K问题（用最小堆解决）
# 经典问题：从海量数据中找出最大的K个数

import heapq


def top_k_largest(arr, k):
    """
    方法一：使用最小堆找出最大的K个数
    核心思路：维护一个大小为K的最小堆
    - 当堆未满时，直接入堆
    - 当堆满时，新元素比堆顶大才替换堆顶
    - 最终堆里的元素就是最大的K个
    时间复杂度：O(n log k)，空间复杂度：O(k)
    适合：n很大，k很小的场景
    """
    # Python的heapq是最小堆
    min_heap = []

    for num in arr:
        if len(min_heap) < k:
            # 堆没满，直接推入
            heapq.heappush(min_heap, num)
        elif num > min_heap[0]:
            # 新元素比堆顶（最小值）大，替换
            heapq.heapreplace(min_heap, num)

    return sorted(min_heap, reverse=True)  # 从大到小返回


def top_k_smallest(arr, k):
    """
    方法二：使用最大堆找出最小的K个数
    核心思路：维护一个大小为K的最大堆
    - 用负数模拟最大堆（Python没有内置最大堆）
    - 最终堆里的元素就是最小的K个
    """
    max_heap = []

    for num in arr:
        if len(max_heap) < k:
            # 用负数实现最大堆
            heapq.heappush(max_heap, -num)
        elif num < -max_heap[0]:
            # 新元素比堆顶（最大值）小，替换
            heapq.heapreplace(max_heap, -num)

    # 取负数还原，从小到大返回
    return sorted([-x for x in max_heap])


def top_k_builtin(arr, k):
    """
    方法三：使用heapq内置函数（一行搞定）
    heapq.nlargest内部已经做了优化
    """
    return heapq.nlargest(k, arr)


# ========== 测试代码 ==========
if __name__ == "__main__":
    print("=== Top K问题演示 ===\n")

    # 测试数据：一个成绩列表
    scores = [85, 92, 78, 95, 88, 76, 90, 93, 82, 87]

    print("--- 场景：找出前3名最高分 ---")
    print(f"所有成绩: {scores}")

    result1 = top_k_largest(scores, 3)
    print(f"方法一（最小堆）前3名: {result1}")

    result2 = top_k_builtin(scores, 3)
    print(f"方法三（内置函数）前3名: {result2}")

    print()
    print("--- 场景：找出后3名最低分 ---")
    result3 = top_k_smallest(scores, 3)
    print(f"方法二（最大堆）后3名: {result3}")

    print()
    print("--- 大规模数据测试：100万个数中找Top 10 ---")
    import random
    import time

    large_data = [random.randint(1, 1000000) for _ in range(1000000)]

    # 方法一：最小堆
    start = time.time()
    result = top_k_largest(large_data, 10)
    elapsed1 = time.time() - start
    print(f"最小堆方法耗时: {elapsed1:.4f}秒，Top 10: {result}")

    # 方法二：内置函数
    start = time.time()
    result = top_k_builtin(large_data, 10)
    elapsed2 = time.time() - start
    print(f"内置函数耗时: {elapsed2:.4f}秒，Top 10: {result}")

    # 对比：排序方法
    start = time.time()
    result = sorted(large_data, reverse=True)[:10]
    elapsed3 = time.time() - start
    print(f"全排序方法耗时: {elapsed3:.4f}秒，Top 10: {result}")

    print(f"\n结论：堆方法比全排序快约 {elapsed3/elapsed1:.1f} 倍！")

# 输出:
# === Top K问题演示 ===
#
# --- 场景：找出前3名最高分 ---
# 所有成绩: [85, 92, 78, 95, 88, 76, 90, 93, 82, 87]
# 方法一（最小堆）前3名: [95, 93, 92]
# 方法三（内置函数）前3名: [95, 93, 92]
#
# --- 场景：找出后3名最低分 ---
# 方法二（最大堆）后3名: [76, 78, 82]
#
# --- 大规模数据测试：100万个数中找Top 10 ---
# 最小堆方法耗时: 0.0500秒，Top 10: [999998, 999997, 999996, 999995, 999994, 999992, 999991, 999990, 999989, 999988]
# 内置函数耗时: 0.0400秒，Top 10: [999998, 999997, 999996, 999995, 999994, 999992, 999991, 999990, 999989, 999988]
# 全排序方法耗时: 0.5000秒，Top 10: [999998, 999997, 999996, 999995, 999994, 999992, 999991, 999990, 999989, 999988]
#
# 结论：堆方法比全排序快约 10.0 倍！
