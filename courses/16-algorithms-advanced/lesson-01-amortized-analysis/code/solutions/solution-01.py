#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：动态数组摊销分析完整实现

这个文件提供了动态数组的完整实现，包含详细的摊销分析。
"""

class DynamicArray:
    """
    动态数组类，支持自动扩容和详细的代价跟踪

    Attributes:
        capacity (int): 当前数组容量
        size (int): 当前元素数量
        array (list): 底层数组
        total_actual_cost (int): 总实际操作代价
        operation_log (list): 操作日志
    """

    def __init__(self, initial_capacity=1):
        """初始化动态数组"""
        self.capacity = initial_capacity
        self.size = 0
        self.array = [None] * self.capacity
        self.total_actual_cost = 0
        self.operation_log = []
        print(f"初始化动态数组: 容量={self.capacity}, 大小={self.size}")

    def _resize(self, new_capacity):
        """
        扩容到新容量

        Args:
            new_capacity (int): 新容量

        Returns:
            int: 扩容操作的实际代价
        """
        if new_capacity <= self.size:
            raise ValueError("新容量不能小于当前大小")

        # 计算扩容代价（复制所有现有元素）
        resize_cost = self.size
        self.total_actual_cost += resize_cost

        # 执行扩容
        old_array = self.array
        self.array = [None] * new_capacity
        for i in range(self.size):
            self.array[i] = old_array[i]

        old_capacity = self.capacity
        self.capacity = new_capacity

        operation_info = {
            'type': 'resize',
            'old_capacity': old_capacity,
            'new_capacity': new_capacity,
            'cost': resize_cost,
            'size': self.size
        }
        self.operation_log.append(operation_info)

        print(f"  扩容: {old_capacity} -> {new_capacity}, 代价={resize_cost}")
        return resize_cost

    def append(self, item):
        """
        添加元素到数组末尾

        Args:
            item: 要添加的元素

        Returns:
            int: 实际操作代价
        """
        # 检查是否需要扩容
        if self.size == self.capacity:
            resize_cost = self._resize(2 * self.capacity)
            actual_cost = 1 + resize_cost  # 添加代价 + 扩容代价
            triggered_resize = True
        else:
            actual_cost = 1
            triggered_resize = False

        # 执行添加
        self.array[self.size] = item
        self.size += 1
        self.total_actual_cost += 1  # 添加操作的代价

        operation_info = {
            'type': 'append',
            'item': item,
            'cost': actual_cost,
            'triggered_resize': triggered_resize,
            'size': self.size,
            'capacity': self.capacity
        }
        self.operation_log.append(operation_info)

        print(f"添加 {item}: 大小={self.size}, 容量={self.capacity}, 代价={actual_cost}")
        return actual_cost

    def get_statistics(self):
        """获取统计信息"""
        total_operations = len([op for op in self.operation_log if op['type'] == 'append'])
        avg_amortized_cost = self.total_actual_cost / total_operations if total_operations > 0 else 0

        return {
            'total_operations': total_operations,
            'total_actual_cost': self.total_actual_cost,
            'average_amortized_cost': avg_amortized_cost,
            'final_size': self.size,
            'final_capacity': self.capacity
        }

def test_dynamic_array():
    """测试动态数组"""
    print("=== 动态数组摊销分析测试 ===\n")

    arr = DynamicArray()

    # 测试序列
    test_data = list(range(20))
    for item in test_data:
        arr.append(item)

    # 显示结果
    stats = arr.get_statistics()
    print(f"\n=== 测试结果 ===")
    print(f"总操作次数: {stats['total_operations']}")
    print(f"总实际代价: {stats['total_actual_cost']}")
    print(f"平均摊销代价: {stats['average_amortized_cost']:.2f}")
    print(f"最终状态: 大小={stats['final_size']}, 容量={stats['final_capacity']}")

    # 验证理论界限
    theoretical_upper_bound = 3 * stats['total_operations']
    print(f"理论上限 (3n): {theoretical_upper_bound}")
    print(f"实际代价 <= 理论上限: {stats['total_actual_cost'] <= theoretical_upper_bound}")

if __name__ == "__main__":
    test_dynamic_array()

# 预期输出:
# 初始化动态数组: 容量=1, 大小=0
# 添加 0: 大小=1, 容量=1, 代价=1
#   扩容: 1 -> 2, 代价=1
# 添加 1: 大小=2, 容量=2, 代价=2
#   扩容: 2 -> 4, 代价=2
# ...
# 总操作次数: 20
# 总实际代价: 57
# 平均摊销代价: 2.85
# 理论上限 (3n): 60
# 实际代价 <= 理论上限: True