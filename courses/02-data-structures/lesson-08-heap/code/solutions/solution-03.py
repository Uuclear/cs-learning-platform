# 解答3：数据流的中位数

import heapq


class MedianFinder:
    """
    使用双堆维护数据流的中位数
    核心思路：
    - max_heap（最大堆）：存储较小的一半数字，用负数模拟
    - min_heap（最小堆）：存储较大的一半数字
    - 保持两个堆大小之差不超过1
    - 中位数：奇数时为多的那个堆的堆顶，偶数时为两堆顶的平均

    时间复杂度：
    - addNum: O(log n)
    - findMedian: O(1)
    """

    def __init__(self):
        # 最大堆（存较小的一半），用负数模拟
        self.max_heap = []
        # 最小堆（存较大的一半）
        self.min_heap = []

    def add_num(self, num):
        """
        添加数字到数据结构中
        策略：先放入最大堆，再平衡到最小堆
        """
        # 先把数字放入最大堆（较小的一半）
        # 注意：用负数实现最大堆
        heapq.heappush(self.max_heap, -num)

        # 保证最大堆的最大值 <= 最小堆的最小值
        # 如果不满足，交换两个堆的堆顶
        if self.max_heap and self.min_heap and -self.max_heap[0] > self.min_heap[0]:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        # 平衡两个堆的大小（差值不超过1）
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, val)

        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def find_median(self):
        """
        返回当前中位数
        - 如果两个堆大小相等，取两堆顶的平均值
        - 如果不等，中位数在较大的堆的堆顶
        """
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        elif len(self.min_heap) > len(self.max_heap):
            return self.min_heap[0]
        else:
            # 大小相等，返回两个堆顶的平均值
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

    def __str__(self):
        """打印当前状态"""
        smaller = sorted([-x for x in self.max_heap])
        larger = sorted(self.min_heap)
        return f"较小部分: {smaller}, 较大部分: {larger}, 中位数: {self.find_median()}"


if __name__ == "__main__":
    print("=== 数据流中位数 ===\n")

    mf = MedianFinder()

    operations = [
        (1, "addNum(1)"),
        (2, "addNum(2)"),
        (None, "findMedian()"),
        (3, "addNum(3)"),
        (None, "findMedian()"),
        (4, "addNum(4)"),
        (None, "findMedian()"),
        (5, "addNum(5)"),
        (None, "findMedian()"),
    ]

    for num, op in operations:
        print(f"操作: {op}")
        if num is not None:
            mf.add_num(num)
        else:
            median = mf.find_median()
            print(f"  -> 中位数: {median}")
        print(f"  状态: {mf}")
        print()

    # 输出:
    # === 数据流中位数 ===
    #
    # 操作: addNum(1)
    #   状态: 较小部分: [1], 较大部分: [], 中位数: 1
    #
    # 操作: addNum(2)
    #   状态: 较小部分: [1], 较大部分: [2], 中位数: 1.5
    #
    # 操作: findMedian()
    #   -> 中位数: 1.5
    #   状态: 较小部分: [1], 较大部分: [2], 中位数: 1.5
    #
    # 操作: addNum(3)
    #   状态: 较小部分: [1, 2], 较大部分: [3], 中位数: 2
    #
    # 操作: findMedian()
    #   -> 中位数: 2
    #   状态: 较小部分: [1, 2], 较大部分: [3], 中位数: 2
    #
    # 操作: addNum(4)
    #   状态: 较小部分: [1, 2], 较大部分: [3, 4], 中位数: 2.5
    #
    # 操作: findMedian()
    #   -> 中位数: 2.5
    #   状态: 较小部分: [1, 2], 较大部分: [3, 4], 中位数: 2.5
    #
    # 操作: addNum(5)
    #   状态: 较小部分: [1, 2, 3], 较大部分: [4, 5], 中位数: 3
    #
    # 操作: findMedian()
    #   -> 中位数: 3
    #   状态: 较小部分: [1, 2, 3], 较大部分: [4, 5], 中位数: 3
