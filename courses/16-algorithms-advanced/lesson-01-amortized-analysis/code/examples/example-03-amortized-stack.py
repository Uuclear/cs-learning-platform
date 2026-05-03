#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：摊销栈实现（支持多弹出操作）

这个文件实现了支持multipop操作的栈，并使用会计方法
分析其摊销时间复杂度。
"""

class AmortizedStack:
    """
    支持摊销分析的栈类

    Attributes:
        stack (list): 底层栈存储
        total_actual_cost (int): 总实际操作代价
        operation_log (list): 操作日志，记录每次操作的详细信息
    """

    def __init__(self):
        """初始化空栈"""
        self.stack = []
        self.total_actual_cost = 0
        self.operation_log = []
        print("初始化摊销栈")

    def push(self, item):
        """
        压入元素到栈顶

        Args:
            item: 要压入的元素

        Returns:
            int: 实际操作代价（总是1）
        """
        self.stack.append(item)
        actual_cost = 1
        self.total_actual_cost += actual_cost

        operation_info = {
            'type': 'push',
            'item': item,
            'actual_cost': actual_cost,
            'stack_size': len(self.stack)
        }
        self.operation_log.append(operation_info)

        print(f"Push({item}): 栈大小={len(self.stack)}, 代价={actual_cost}")
        return actual_cost

    def pop(self):
        """
        弹出栈顶元素

        Returns:
            tuple: (弹出的元素, 实际操作代价) 或 (None, 0) 如果栈为空
        """
        if not self.stack:
            print("栈为空，无法弹出")
            return None, 0

        item = self.stack.pop()
        actual_cost = 1
        self.total_actual_cost += actual_cost

        operation_info = {
            'type': 'pop',
            'item': item,
            'actual_cost': actual_cost,
            'stack_size': len(self.stack)
        }
        self.operation_log.append(operation_info)

        print(f"Pop(): 弹出={item}, 栈大小={len(self.stack)}, 代价={actual_cost}")
        return item, actual_cost

    def multipop(self, k):
        """
        弹出最多k个元素

        Args:
            k (int): 最大弹出数量

        Returns:
            tuple: (弹出的元素列表, 实际操作代价)
        """
        if k <= 0:
            print("multipop参数无效")
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
                'items': popped_items,
                'actual_cost': actual_cost,
                'stack_size': len(self.stack)
            }
            self.operation_log.append(operation_info)

        print(f"Multipop({k}): 请求={k}, 实际={actual_pops}, 栈大小={len(self.stack)}, 代价={actual_cost}")
        return popped_items, actual_cost

    def get_statistics(self):
        """
        获取操作统计信息

        Returns:
            dict: 包含总操作数、总代价、平均摊销代价等信息的字典
        """
        total_operations = len(self.operation_log)
        avg_amortized_cost = self.total_actual_cost / total_operations if total_operations > 0 else 0

        # 统计各类操作的数量
        operation_counts = {'push': 0, 'pop': 0, 'multipop': 0}
        for op in self.operation_log:
            operation_counts[op['type']] += 1

        return {
            'total_operations': total_operations,
            'total_actual_cost': self.total_actual_cost,
            'average_amortized_cost': avg_amortized_cost,
            'operation_counts': operation_counts,
            'final_stack_size': len(self.stack)
        }

def demonstrate_amortized_stack():
    """演示摊销栈的操作序列和分析"""
    print("=== 摊销栈演示 ===\n")

    stack = AmortizedStack()

    # 执行一系列混合操作
    operations_sequence = [
        ('push', 1),
        ('push', 2),
        ('push', 3),
        ('push', 4),
        ('push', 5),
        ('multipop', 2),
        ('push', 6),
        ('multipop', 10),  # 尝试弹出超过栈大小
        ('push', 7),
        ('push', 8),
        ('pop', None),
        ('multipop', 3)
    ]

    for op_type, arg in operations_sequence:
        if op_type == 'push':
            stack.push(arg)
        elif op_type == 'pop':
            stack.pop()
        elif op_type == 'multipop':
            stack.multipop(arg)

    # 显示统计结果
    stats = stack.get_statistics()
    print(f"\n=== 统计结果 ===")
    print(f"总操作次数: {stats['total_operations']}")
    print(f"总实际代价: {stats['total_actual_cost']}")
    print(f"平均摊销代价: {stats['average_amortized_cost']:.2f}")
    print(f"操作分布: {stats['operation_counts']}")
    print(f"最终栈大小: {stats['final_stack_size']}")

def main():
    """主函数"""
    demonstrate_amortized_stack()

if __name__ == "__main__":
    main()

# 预期输出示例:
# 初始化摊销栈
# Push(1): 栈大小=1, 代价=1
# Push(2): 栈大小=2, 代价=1
# Push(3): 栈大小=3, 代价=1
# Push(4): 栈大小=4, 代价=1
# Push(5): 栈大小=5, 代价=1
# Multipop(2): 请求=2, 实际=2, 栈大小=3, 代价=2
# Push(6): 栈大小=4, 代价=1
# Multipop(10): 请求=10, 实际=4, 栈大小=0, 代价=4
# ...
# 总操作次数: 12
# 总实际代价: 14
# 平均摊销代价: 1.17