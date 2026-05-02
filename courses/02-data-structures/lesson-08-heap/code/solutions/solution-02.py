# 解答2：滑动窗口最大值

import heapq


def max_sliding_window(nums, k):
    """
    使用最大堆解决滑动窗口最大值问题
    核心思路：堆中存储(-值, 索引)，每次取堆顶时检查是否在窗口内
    时间复杂度：O(n log n)
    空间复杂度：O(n)

    注意：更优的方案是用单调队列O(n)，但堆方法更容易理解
    """
    if not nums or k <= 0:
        return []

    n = len(nums)
    if k == 1:
        return nums

    result = []

    # Python只有最小堆，用负数模拟最大堆
    # 堆中存储 (-值, 索引)
    max_heap = []

    for i in range(n):
        # 将当前元素放入堆
        heapq.heappush(max_heap, (-nums[i], i))

        # 窗口形成后（至少k个元素）才开始记录结果
        if i >= k - 1:
            # 移除堆顶的过期元素（索引不在当前窗口内）
            while max_heap[0][1] <= i - k:
                heapq.heappop(max_heap)

            # 堆顶就是当前窗口的最大值
            result.append(-max_heap[0][0])

    return result


def max_sliding_window_verbose(nums, k):
    """带可视化步骤的版本"""
    if not nums or k <= 0:
        return []

    n = len(nums)
    result = []
    max_heap = []

    print(f"数组: {nums}, 窗口大小: {k}")
    print()

    for i in range(n):
        heapq.heappush(max_heap, (-nums[i], i))

        if i >= k - 1:
            # 清除过期元素
            while max_heap[0][1] <= i - k:
                removed = heapq.heappop(max_heap)
                print(f"  窗口[{i-k+1}..{i}]，移除过期元素({-removed[0]}, 索引{removed[1]})")

            window_start = i - k + 1
            max_val = -max_heap[0][0]
            result.append(max_val)
            print(f"  窗口[{window_start}..{i}] = {nums[window_start:i+1]}，最大值: {max_val}")

    return result


if __name__ == "__main__":
    print("=== 滑动窗口最大值 ===\n")

    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3

    result = max_sliding_window_verbose(nums, k)
    print(f"\n最终结果: {result}")

    # 输出:
    # === 滑动窗口最大值 ===
    #
    # 数组: [1, 3, -1, -3, 5, 3, 6, 7], 窗口大小: 3
    #
    #   窗口[0..2] = [1, 3, -1]，最大值: 3
    #   窗口[1..3] = [3, -1, -3]，最大值: 3
    #   窗口[2..4] = [-1, -3, 5]，最大值: 5
    #   窗口[3..5] = [-3, 5, 3]，最大值: 5
    #   窗口[4..6] = [5, 3, 6]，最大值: 6
    #   窗口[5..7] = [3, 6, 7]，最大值: 7
    #
    # 最终结果: [3, 3, 5, 5, 6, 7]
