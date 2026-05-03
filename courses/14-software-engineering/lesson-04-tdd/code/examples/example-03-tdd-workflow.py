#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDD 完整工作流演示

这个例子展示了完整的TDD工作流，包括测试设计、实现、重构的全过程。
我们实现一个功能完整的计算器类，并通过全面的测试来保证其正确性。
"""

import unittest


class Calculator:
    """计算器类，支持基本的四则运算"""

    def add(self, a, b):
        """
        加法运算

        Args:
            a (float): 第一个操作数
            b (float): 第二个操作数

        Returns:
            float: 两个数的和

        Examples:
            >>> calc = Calculator()
            >>> calc.add(2, 3)
            5
            >>> calc.add(-1, 1)
            0
        """
        return a + b

    def subtract(self, a, b):
        """
        减法运算

        Args:
            a (float): 被减数
            b (float): 减数

        Returns:
            float: 差值

        Examples:
            >>> calc = Calculator()
            >>> calc.subtract(5, 3)
            2
            >>> calc.subtract(0, 5)
            -5
        """
        return a - b

    def multiply(self, a, b):
        """
        乘法运算

        Args:
            a (float): 第一个因子
            b (float): 第二个因子

        Returns:
            float: 乘积

        Examples:
            >>> calc = Calculator()
            >>> calc.multiply(4, 3)
            12
            >>> calc.multiply(-2, 3)
            -6
        """
        return a * b

    def divide(self, a, b):
        """
        除法运算

        Args:
            a (float): 被除数
            b (float): 除数

        Returns:
            float: 商

        Raises:
            ValueError: 当除数为零时抛出异常

        Examples:
            >>> calc = Calculator()
            >>> calc.divide(10, 2)
            5.0
            >>> calc.divide(7, 2)
            3.5
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b

    def power(self, base, exponent):
        """
        幂运算

        Args:
            base (float): 底数
            exponent (float): 指数

        Returns:
            float: 幂的结果

        Examples:
            >>> calc = Calculator()
            >>> calc.power(2, 3)
            8
            >>> calc.power(5, 0)
            1
        """
        return base ** exponent

    def sqrt(self, number):
        """
        平方根运算

        Args:
            number (float): 被开方数

        Returns:
            float: 平方根

        Raises:
            ValueError: 当被开方数为负数时抛出异常

        Examples:
            >>> calc = Calculator()
            >>> calc.sqrt(9)
            3.0
            >>> calc.sqrt(0)
            0.0
        """
        if number < 0:
            raise ValueError("负数不能开平方根")
        return number ** 0.5


class TestCalculator(unittest.TestCase):
    """计算器的完整测试套件"""

    def setUp(self):
        """测试前准备：创建计算器实例"""
        self.calc = Calculator()

    # ==================== 加法测试 ====================
    def test_add_positive_numbers(self):
        """测试正数相加"""
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_add_negative_numbers(self):
        """测试负数相加"""
        self.assertEqual(self.calc.add(-2, -3), -5)

    def test_add_positive_and_negative(self):
        """测试正负数相加"""
        self.assertEqual(self.calc.add(5, -3), 2)
        self.assertEqual(self.calc.add(-5, 3), -2)

    def test_add_with_zero(self):
        """测试与零相加"""
        self.assertEqual(self.calc.add(5, 0), 5)
        self.assertEqual(self.calc.add(0, -3), -3)

    def test_add_floating_point(self):
        """测试浮点数相加"""
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=7)

    # ==================== 减法测试 ====================
    def test_subtract_positive_numbers(self):
        """测试正数相减"""
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_subtract_negative_result(self):
        """测试结果为负数的减法"""
        self.assertEqual(self.calc.subtract(3, 5), -2)

    def test_subtract_negative_numbers(self):
        """测试负数相减"""
        self.assertEqual(self.calc.subtract(-3, -5), 2)

    def test_subtract_with_zero(self):
        """测试与零相减"""
        self.assertEqual(self.calc.subtract(5, 0), 5)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    # ==================== 乘法测试 ====================
    def test_multiply_positive_numbers(self):
        """测试正数相乘"""
        self.assertEqual(self.calc.multiply(4, 3), 12)

    def test_multiply_by_zero(self):
        """测试与零相乘"""
        self.assertEqual(self.calc.multiply(5, 0), 0)

    def test_multiply_negative_numbers(self):
        """测试负数相乘"""
        self.assertEqual(self.calc.multiply(-4, -3), 12)
        self.assertEqual(self.calc.multiply(-4, 3), -12)

    def test_multiply_floating_point(self):
        """测试浮点数相乘"""
        self.assertAlmostEqual(self.calc.multiply(0.5, 0.4), 0.2, places=7)

    # ==================== 除法测试 ====================
    def test_divide_positive_numbers(self):
        """测试正数相除"""
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_negative_numbers(self):
        """测试负数相除"""
        self.assertEqual(self.calc.divide(-10, 2), -5.0)
        self.assertEqual(self.calc.divide(-10, -2), 5.0)

    def test_divide_floating_point(self):
        """测试浮点数相除"""
        self.assertAlmostEqual(self.calc.divide(7, 2), 3.5, places=7)

    def test_divide_by_zero_raises_exception(self):
        """测试除零异常"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)

        self.assertEqual(str(context.exception), "除数不能为零")

    # ==================== 幂运算测试 ====================
    def test_power_positive_exponent(self):
        """测试正指数幂运算"""
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_power_zero_exponent(self):
        """测试零指数幂运算"""
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_power_negative_exponent(self):
        """测试负指数幂运算"""
        self.assertAlmostEqual(self.calc.power(2, -1), 0.5, places=7)

    def test_power_zero_base(self):
        """测试零底数幂运算"""
        self.assertEqual(self.calc.power(0, 5), 0)
        self.assertEqual(self.calc.power(0, 0), 1)  # 0^0 在Python中定义为1

    # ==================== 平方根测试 ====================
    def test_sqrt_positive_number(self):
        """测试正数平方根"""
        self.assertEqual(self.calc.sqrt(9), 3.0)
        self.assertEqual(self.calc.sqrt(0), 0.0)

    def test_sqrt_floating_point(self):
        """测试浮点数平方根"""
        self.assertAlmostEqual(self.calc.sqrt(2), 1.4142135623730951, places=10)

    def test_sqrt_negative_number_raises_exception(self):
        """测试负数平方根异常"""
        with self.assertRaises(ValueError) as context:
            self.calc.sqrt(-1)

        self.assertEqual(str(context.exception), "负数不能开平方根")


class TestCalculatorEdgeCases(unittest.TestCase):
    """计算器边界情况测试"""

    def setUp(self):
        self.calc = Calculator()

    def test_large_numbers(self):
        """测试大数运算"""
        large_num = 10**10
        self.assertEqual(self.calc.add(large_num, large_num), 2 * large_num)

    def test_very_small_numbers(self):
        """测试极小数运算"""
        small_num = 1e-10
        result = self.calc.add(small_num, small_num)
        self.assertAlmostEqual(result, 2e-10, places=15)


if __name__ == '__main__':
    # 运行所有测试，显示详细信息
    unittest.main(verbosity=2)