#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：动态数组摊销分析演示

这个文件演示了动态数组的实现和摊销分析过程。
通过跟踪每次操作的实际代价和累计代价，展示为什么
动态数组的append操作具有O(1)的摊销时间复杂度。
"""

class DynamicArray:
    """
    动态数组类，支持自动扩容

    Attributes:
        capacity (int): 当前数组容量
        size (int): 当前存储的元素数量
        array (list): 底层数组存储
        total_cost (int): 累计操作代价，用于分析
    """

    def __init__(self):
        """初始化动态数组，初始容量为1"""
        self.capacity = 1
        self.size = 0
        self.array = [None] * self.capacity
        self.total_cost = 0
        print(f"初始化动态数组: 容量={self.capacity}, 大小={self.size}")

    def _resize(self, new_capacity):
        """
        扩容数组到新的容量

        Args:
            new_capacity (int): 新的数组容量

        Returns:
            int: 扩容操作的实际代价（等于复制的元素数量）
        """
        # 记录扩容代价：需要复制所有现有元素
        resize_cost = self.size
        self.total_cost += resize_cost

        # 执行实际的扩容操作
        old_array = self.array
        self.array = [None] * new_capacity
        for i in range(self.size):
            self.array[i] = old_array[i]

        old_capacity = self.capacity
        self.capacity = new_capacity
        print(f"  扩容操作: {old_capacity} -> {new_capacity}, 代价={resize_cost}")
        return resize_cost

    def append(self, item):
        """
        在数组末尾添加元素

        Args:
            item: 要添加的元素

        Returns:
            tuple: (实际代价, 是否触发扩容)
        """
        # 检查是否需要扩容
        if self.size == self.capacity:
            resize_cost = self._resize(2 * self.capacity)
            # append本身的代价 + 扩容代价
            actual_cost = 1 + resize_cost
            triggered_resize = True
        else:
            actual_cost = 1
            triggered_resize = False

        # 执行实际的添加操作
        self.array[self.size] = item
        self.size += 1
        self.total_cost += 1  # 添加元素的代价

        print(f"添加元素 {item}: 大小={self.size}, 容量={self.capacity}, 实际代价={actual_cost}")
        return actual_cost, triggered_resize

def main():
    """主函数：演示动态数组的摊销分析"""
    print("=== 动态数组摊销分析演示 ===\n")

    # 创建动态数组实例
    arr = DynamicArray()

    # 执行一系列append操作
    operations = []
    for i in range(12):
        cost, resized = arr.append(i)
        operations.append((i, cost, resized))

    # 分析结果
    print(f"\n=== 分析结果 ===")
    print(f"总操作次数: {len(operations)}")
    print(f"总实际代价: {arr.total_cost}")
    print(f"平均摊销代价: {arr.total_cost / len(operations):.2f}")

    # 显示详细操作记录
    print(f"\n详细操作记录:")
    cumulative_cost = 0
    for i, (value, cost, resized) in enumerate(operations):
        cumulative_cost += cost
        amortized_so_far = cumulative_cost / (i + 1)
        resize_str = " (扩容)" if resized else ""
        print(f"  操作 {i+1}: 添加 {value}, 代价={cost}{resize_str}, 累计代价={cumulative_cost}, 平均={amortized_so_far:.2f}")

if __name__ == "__main__":
    main()

# 预期输出示例:
# 初始化动态数组: 容量=1, 大小=0
# 添加元素 0: 大小=1, 容量=1, 实际代价=1
#   扩容操作: 1 -> 2, 代价=1
# 添加元素 1: 大小=2, 容量=2, 实际代价=2
#   扩容操作: 2 -> 4, 代价=2
# 添加元素 2: 大小=3, 容量=4, 实际代价=1
# 添加元素 3: 大小=4, 容量=4, 实际代价=1
#   扩容操作: 4 -> 8, 代价=4
# ...
# 总实际代价: 25
# 平均摊销代价: 2.08