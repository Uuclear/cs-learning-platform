#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试示例：演示如何编写有效的单元测试

本文件展示了：
1. 使用 unittest 框架的基本结构
2. AAA 测试模式（Arrange-Act-Assert）
3. 使用 mock 模拟外部依赖
4. 测试边界条件和异常情况
"""

import unittest
from unittest.mock import Mock, patch


class Calculator:
    """简单的计算器类"""

    def add(self, a, b):
        """加法运算"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("参数必须是数字")
        return a + b

    def divide(self, a, b):
        """除法运算"""
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b


class UserService:
    """用户服务类，依赖外部组件"""

    def __init__(self, email_service, logger):
        self.email_service = email_service
        self.logger = logger

    def create_user(self, username, email):
        """创建用户并发送欢迎邮件"""
        # 验证输入
        if not username or not email:
            raise ValueError("用户名和邮箱不能为空")

        # 创建用户逻辑（这里简化为字典）
        user = {
            'username': username,
            'email': email,
            'status': 'active'
        }

        # 发送欢迎邮件
        try:
            self.email_service.send_welcome_email(email, username)
            self.logger.info(f"用户 {username} 创建成功，欢迎邮件已发送")
        except Exception as e:
            self.logger.error(f"发送欢迎邮件失败: {e}")
            # 注意：这里我们选择继续创建用户，但记录错误

        return user


class TestCalculator(unittest.TestCase):
    """计算器单元测试"""

    def setUp(self):
        """测试前准备"""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """测试正数相加"""
        # Arrange - 准备数据
        a, b = 2, 3
        expected = 5

        # Act - 执行操作
        result = self.calc.add(a, b)

        # Assert - 验证结果
        self.assertEqual(result, expected)

    def test_add_negative_numbers(self):
        """测试负数相加"""
        result = self.calc.add(-1, -2)
        self.assertEqual(result, -3)

    def test_add_with_floats(self):
        """测试浮点数相加"""
        result = self.calc.add(1.5, 2.5)
        self.assertEqual(result, 4.0)

    def test_add_invalid_type_raises_error(self):
        """测试无效类型参数抛出异常"""
        with self.assertRaises(TypeError):
            self.calc.add("1", 2)

    def test_divide_normal_case(self):
        """测试正常除法"""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_divide_by_zero_raises_error(self):
        """测试除零异常"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)


class TestUserService(unittest.TestCase):
    """用户服务单元测试"""

    def setUp(self):
        """设置模拟对象"""
        self.mock_email_service = Mock()
        self.mock_logger = Mock()
        self.user_service = UserService(self.mock_email_service, self.mock_logger)

    def test_create_user_success(self):
        """测试成功创建用户"""
        # Arrange
        username = "testuser"
        email = "test@example.com"

        # Act
        user = self.user_service.create_user(username, email)

        # Assert
        self.assertEqual(user['username'], username)
        self.assertEqual(user['email'], email)
        self.assertEqual(user['status'], 'active')

        # 验证邮件服务被正确调用
        self.mock_email_service.send_welcome_email.assert_called_once_with(email, username)

        # 验证日志被正确记录
        self.mock_logger.info.assert_called_once()

    def test_create_user_empty_username_raises_error(self):
        """测试空用户名抛出异常"""
        with self.assertRaises(ValueError):
            self.user_service.create_user("", "test@example.com")

    def test_create_user_empty_email_raises_error(self):
        """测试空邮箱抛出异常"""
        with self.assertRaises(ValueError):
            self.user_service.create_user("testuser", "")

    def test_create_user_email_failure_continues(self):
        """测试邮件发送失败时仍创建用户"""
        # 安排邮件服务抛出异常
        self.mock_email_service.send_welcome_email.side_effect = Exception("邮件服务器错误")

        # 执行创建用户
        user = self.user_service.create_user("testuser", "test@example.com")

        # 验证用户仍然被创建
        self.assertEqual(user['username'], "testuser")

        # 验证错误被记录
        self.mock_logger.error.assert_called_once()


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)