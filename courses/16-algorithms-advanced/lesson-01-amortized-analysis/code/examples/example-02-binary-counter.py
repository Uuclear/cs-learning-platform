#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：二进制计数器摊销分析

这个文件实现了二进制计数器，并演示了如何使用聚合方法
分析increment操作的摊销时间复杂度。
"""

class BinaryCounter:
    """
    二进制计数器类

    Attributes:
        bits (list): 二进制位数组，bits[0]是最低有效位
        total_flips (int): 总翻转次数
        num_bits (int): 计数器总位数
    """

    def __init__(self, num_bits=8):
        """
        初始化二进制计数器

        Args:
            num_bits (int): 计数器的位数，默认为8位
        """
        self.bits = [0] * num_bits
        self.total_flips = 0
        self.num_bits = num_bits
        print(f"初始化 {num_bits} 位二进制计数器: {self._get_binary_string()}")

    def _get_binary_string(self):
        """
        获取当前二进制字符串表示（高位在前）

        Returns:
            str: 二进制字符串
        """
        return ''.join(map(str, reversed(self.bits)))

    def increment(self):
        """
        递增计数器值

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

        # 如果还有位可以设置，将第一个0设为1
        if i < self.num_bits:
            self.bits[i] = 1
            flips += 1

        self.total_flips += flips
        print(f"递增后: {self._get_binary_string()} (翻转 {flips} 位)")
        return flips

    def get_total_flips(self):
        """
        获取总翻转次数

        Returns:
            int: 总翻转次数
        """
        return self.total_flips

def analyze_amortized_cost(num_increments, num_bits=8):
    """
    分析二进制计数器的摊销代价

    Args:
        num_increments (int): 递增操作次数
        num_bits (int): 计数器位数

    Returns:
        tuple: (总翻转次数, 平均摊销代价)
    """
    print(f"=== 二进制计数器摊销分析 ({num_increments} 次递增) ===\n")

    counter = BinaryCounter(num_bits)
    flip_history = []

    for i in range(num_increments):
        flips = counter.increment()
        flip_history.append(flips)

        # 每4次操作显示一次累计统计
        if (i + 1) % 4 == 0 or i == num_increments - 1:
            total_so_far = sum(flip_history)
            avg_so_far = total_so_far / (i + 1)
            print(f"  前 {i+1} 次操作: 总翻转={total_so_far}, 平均={avg_so_far:.2f}")

    total_flips = counter.get_total_flips()
    amortized_cost = total_flips / num_increments if num_increments > 0 else 0

    print(f"\n=== 最终结果 ===")
    print(f"总递增次数: {num_increments}")
    print(f"总翻转次数: {total_flips}")
    print(f"平均摊销代价: {amortized_cost:.2f}")

    # 理论分析验证
    theoretical_max = 2 * num_increments  # 理论上界
    print(f"理论上限 (2n): {theoretical_max}")
    print(f"实际/理论比例: {total_flips/theoretical_max:.2f}")

    return total_flips, amortized_cost

def main():
    """主函数：运行二进制计数器分析"""
    # 分析不同规模的操作序列
    test_cases = [8, 16, 32, 64]

    for n in test_cases:
        analyze_amortized_cost(n, num_bits=8)
        print()

if __name__ == "__main__":
    main()

# 预期输出示例:
# 初始化 8 位二进制计数器: 00000000
# 递增后: 00000001 (翻转 1 位)
# 递增后: 00000010 (翻转 2 位)
# 递增后: 00000011 (翻转 1 位)
# 递增后: 00000100 (翻转 3 位)
#   前 4 次操作: 总翻转=7, 平均=1.75
# ...
# 总递增次数: 16
# 总翻转次数: 30
# 平均摊销代价: 1.88
# 理论上限 (2n): 32
# 实际/理论比例: 0.94