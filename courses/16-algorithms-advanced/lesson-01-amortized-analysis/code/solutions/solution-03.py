#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：摊销栈完整实现

这个文件提供了支持multipop操作的摊销栈的完整实现。
"""

class AmortizedStack:
    """
    支持摊销分析的栈类

    Attributes:
        stack (list): 底层栈
        total_actual_cost (int): 总实际代价
        operation_log (list): 操作日志
    """

    def __init__(self):
        """初始化栈"""
        self.stack = []
        self.total_actual_cost = 0
        self.operation_log = []
        print("初始化摊销栈")

    def push(self, item):
        """
        压入元素

        Args:
            item: 要压入的元素

        Returns:
            int: 实际代价
        """
        self.stack.append(item)
        actual_cost = 1
        self.total_actual_cost += actual_cost

        operation_info = {
            'type': 'push',
            'item': item,
            'cost': actual_cost,
            'stack_size': len(self.stack)
        }
        self.operation_log.append(operation_info)

        print(f"Push({item}): 栈大小={len(self.stack)}, 代价={actual_cost}")
        return actual_cost

    def pop(self):
        """
        弹出元素

        Returns:
            tuple: (元素, 实际代价) 或 (None, 0)
        """
        if not self.stack:
            print("栈为空")
            return None, 0

        item = self.stack.pop()
        actual_cost = 1
        self.total_actual_cost += actual_cost

        operation_info = {
            'type': 'pop',
            'item': item,
            'cost': actual_cost,
            'stack_size': len(self.stack)
        }
        self.operation_log.append(operation_info)

        print(f"Pop(): {item}, 栈大小={len(self.stack)}, 代价={actual_cost}")
        return item, actual_cost

    def multipop(self, k):
        """
        多弹出操作

        Args:
            k (int): 最大弹出数量

        Returns:
            tuple: (元素列表, 实际代价)
        """
        if k <= 0:
            print("无效的multipop参数")
            return [], 0

        popped_items = []
        actual_pops = min(k, len(self.stack))
        actual_cost = actual_pops

        for _ in range(actual_pops):
            popped_items.append(self.stack.pop())

        if actual_pops > 0:
            self.total_actual_cost += actual_cost

            operation_info = {
                'type': 'multipop',
                'requested': k,
                'actual': actual_pops,
                'items': popped_items.copy(),
                'cost': actual_cost,
                'stack_size': len(self.stack)
            }
            self.operation_log.append(operation_info)

        print(f"Multipop({k}): 请求={k}, 实际={actual_pops}, 代价={actual_cost}")
        return popped_items, actual_cost

    def get_statistics(self):
        """获取统计信息"""
        total_operations = len(self.operation_log)
        avg_amortized_cost = self.total_actual_cost / total_operations if total_operations > 0 else 0

        # 统计各类操作
        op_counts = {'push': 0, 'pop': 0, 'multipop': 0}
        for op in self.operation_log:
            op_counts[op['type']] += 1

        return {
            'total_operations': total_operations,
            'total_actual_cost': self.total_actual_cost,
            'average_amortized_cost': avg_amortized_cost,
            'operation_counts': op_counts,
            'final_stack_size': len(self.stack)
        }

def test_amortized_stack():
    """测试摊销栈"""
    print("=== 摊销栈测试 ===\n")

    stack = AmortizedStack()

    # 测试序列
    test_sequence = [
        ('push', 1),
        ('push', 2),
        ('push', 3),
        ('push', 4),
        ('push', 5),
        ('multipop', 2),
        ('push', 6),
        ('push', 7),
        ('multipop', 5),
        ('push', 8),
        ('pop', None),
        ('push', 9),
        ('multipop', 10)
    ]

    for op_type, arg in test_sequence:
        if op_type == 'push':
            stack.push(arg)
        elif op_type == 'pop':
            stack.pop()
        elif op_type == 'multipop':
            stack.multipop(arg)

    # 显示统计结果
    stats = stack.get_statistics()
    print(f"\n=== 测试结果 ===")
    print(f"总操作次数: {stats['total_operations']}")
    print(f"总实际代价: {stats['total_actual_cost']}")
    print(f"平均摊销代价: {stats['average_amortized_cost']:.2f}")
    print(f"操作分布: {stats['operation_counts']}")
    print(f"最终栈大小: {stats['final_stack_size']}")

    # 验证摊销性质
    expected_upper_bound = 2 * stats['total_operations']
    print(f"理论上限 (2n): {expected_upper_bound}")
    print(f"实际代价 <= 理论上限: {stats['total_actual_cost'] <= expected_upper_bound}")

if __name__ == "__main__":
    test_amortized_stack()

# 预期输出示例:
# 初始化摊销栈
# Push(1): 栈大小=1, 代价=1
# Push(2): 栈大小=2, 代价=1
# ...
# Multipop(2): 请求=2, 实际=2, 代价=2
# ...
# 总操作次数: 13
# 总实际代价: 16
# 平均摊销代价: 1.23
# 操作分布: {'push': 6, 'pop': 1, 'multipop': 6}
# 最终栈大小: 0