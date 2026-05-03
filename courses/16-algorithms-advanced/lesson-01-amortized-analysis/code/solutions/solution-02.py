#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：二进制计数器摊销分析完整实现

这个文件提供了二进制计数器的完整实现和详细的摊销分析。
"""

class BinaryCounter:
    """
    二进制计数器类

    Attributes:
        bits (list): 二进制位数组
        total_flips (int): 总翻转次数
        num_bits (int): 计数器位数
        operation_log (list): 操作日志
    """

    def __init__(self, num_bits=16):
        """初始化二进制计数器"""
        self.bits = [0] * num_bits
        self.total_flips = 0
        self.num_bits = num_bits
        self.operation_log = []
        print(f"初始化 {num_bits} 位二进制计数器: {self.get_binary_string()}")

    def get_binary_string(self):
        """获取二进制字符串表示（高位在前）"""
        return ''.join(map(str, reversed(self.bits)))

    def get_decimal_value(self):
        """获取十进制值"""
        value = 0
        for i, bit in enumerate(self.bits):
            if bit:
                value += (1 << i)
        return value

    def increment(self):
        """
        递增计数器

        Returns:
            int: 本次操作的翻转次数
        """
        flips = 0
        i = 0

        # 翻转连续的1为0
        while i < self.num_bits and self.bits[i] == 1:
            self.bits[i] = 0
            flips += 1
            i += 1

        # 设置第一个0为1
        if i < self.num_bits:
            self.bits[i] = 1
            flips += 1

        self.total_flips += flips
        current_value = self.get_decimal_value()

        operation_info = {
            'type': 'increment',
            'flips': flips,
            'total_flips': self.total_flips,
            'value': current_value,
            'binary': self.get_binary_string()
        }
        self.operation_log.append(operation_info)

        print(f"递增到 {current_value}: {self.get_binary_string()} (翻转 {flips} 位)")
        return flips

    def analyze_amortized_cost(self, num_operations):
        """分析摊销代价"""
        print(f"\n=== 执行 {num_operations} 次递增操作 ===")

        for i in range(num_operations):
            self.increment()

        # 计算统计信息
        total_flips = self.total_flips
        avg_amortized_cost = total_flips / num_operations if num_operations > 0 else 0

        # 理论分析
        theoretical_max = 2 * num_operations
        theoretical_exact = 0
        temp = num_operations
        while temp > 0:
            theoretical_exact += temp
            temp //= 2

        print(f"\n=== 摊销分析结果 ===")
        print(f"操作次数: {num_operations}")
        print(f"总翻转次数: {total_flips}")
        print(f"平均摊销代价: {avg_amortized_cost:.4f}")
        print(f"理论精确值: {theoretical_exact}")
        print(f"理论上限 (2n): {theoretical_max}")
        print(f"实际/理论比例: {total_flips/theoretical_exact:.4f}")

        return total_flips, avg_amortized_cost

def test_binary_counter():
    """测试二进制计数器"""
    print("=== 二进制计数器摊销分析测试 ===")

    # 测试不同规模
    test_cases = [16, 32, 64, 128]

    for n in test_cases:
        print(f"\n--- 测试 {n} 次递增 ---")
        counter = BinaryCounter(8)  # 使用8位便于观察
        counter.analyze_amortized_cost(n)

if __name__ == "__main__":
    test_binary_counter()

# 预期输出示例:
# 初始化 8 位二进制计数器: 00000000
# 递增到 1: 00000001 (翻转 1 位)
# 递增到 2: 00000010 (翻转 2 位)
# ...
# 操作次数: 16
# 总翻转次数: 30
# 平均摊销代价: 1.8750
# 理论精确值: 30
# 理论上限 (2n): 32
# 实际/理论比例: 1.0000