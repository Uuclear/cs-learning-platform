#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDD 红-绿-重构循环演示

这个例子展示了如何通过TDD的红-绿-重构循环来实现一个字符串计算器。
我们逐步添加功能，每次只添加一个测试用例，然后让其实现通过。
"""

import unittest


class StringCalculator:
    """字符串计算器类，用于计算以逗号分隔的数字字符串的总和"""

    def add(self, numbers):
        """
        计算数字字符串的总和

        Args:
            numbers (str): 以逗号分隔的数字字符串，例如 "1,2,3"

        Returns:
            int: 所有数字的总和

        Examples:
            >>> calc = StringCalculator()
            >>> calc.add("")  # 空字符串
            0
            >>> calc.add("1")  # 单个数字
            1
            >>> calc.add("1,2")  # 多个数字
            3
        """
        # 处理空字符串的情况
        if not numbers:
            return 0

        # 将字符串按逗号分割并转换为整数，然后求和
        return sum(int(num) for num in numbers.split(","))


class TestStringCalculator(unittest.TestCase):
    """字符串计算器的测试类"""

    def setUp(self):
        """测试前的初始化，创建计算器实例"""
        self.calc = StringCalculator()

    def test_empty_string_returns_zero(self):
        """测试：空字符串应该返回0"""
        result = self.calc.add("")
        self.assertEqual(result, 0)

    def test_single_number_returns_itself(self):
        """测试：单个数字应该返回自身"""
        result = self.calc.add("5")
        self.assertEqual(result, 5)

    def test_two_numbers_return_sum(self):
        """测试：两个数字应该返回它们的和"""
        result = self.calc.add("2,3")
        self.assertEqual(result, 5)

    def test_multiple_numbers_return_sum(self):
        """测试：多个数字应该返回它们的总和"""
        result = self.calc.add("1,2,3,4,5")
        self.assertEqual(result, 15)


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)