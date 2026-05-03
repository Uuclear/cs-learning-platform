#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TDD 测试替身（Mocks, Stubs, Fakes）演示

这个例子展示了在TDD中如何使用不同类型的测试替身来隔离依赖，
使测试更加专注和可靠。
"""

import unittest
from unittest.mock import Mock, patch


# ==================== 被测试的类 ====================

class EmailService:
    """真实的邮件服务类（在实际项目中可能很复杂）"""

    def send_welcome_email(self, email):
        """发送欢迎邮件"""
        # 实际的邮件发送逻辑...
        print(f"发送欢迎邮件到: {email}")
        return True

    def send_notification(self, email, message):
        """发送通知邮件"""
        # 实际的通知发送逻辑...
        print(f"发送通知到 {email}: {message}")
        return True


class UserService:
    """用户服务类，依赖于邮件服务"""

    def __init__(self, email_service):
        """
        初始化用户服务

        Args:
            email_service: 邮件服务实例
        """
        self.email_service = email_service

    def register_user(self, username, email):
        """
        注册新用户并发送欢迎邮件

        Args:
            username (str): 用户名
            email (str): 邮箱地址

        Returns:
            dict: 包含用户信息的字典
        """
        # 保存用户到数据库（这里简化为返回固定值）
        user_id = self._save_user_to_database(username, email)

        # 发送欢迎邮件（处理可能的异常）
        try:
            self.email_service.send_welcome_email(email)
        except Exception as e:
            # 在实际项目中，你可能需要记录日志或重试
            # 但用户注册应该继续成功
            pass

        return {
            "id": user_id,
            "username": username,
            "email": email,
            "status": "active"
        }

    def _save_user_to_database(self, username, email):
        """模拟保存用户到数据库"""
        # 在实际项目中，这里会连接真实数据库
        return 12345


# ==================== 测试替身的实现 ====================

class FakeEmailService:
    """Fake（假对象）：具有简化但真实的实现"""

    def __init__(self):
        self.sent_emails = []

    def send_welcome_email(self, email):
        """简化的邮件发送实现，记录发送的邮件"""
        self.sent_emails.append({"type": "welcome", "email": email})
        return True

    def send_notification(self, email, message):
        """简化的通知发送实现"""
        self.sent_emails.append({"type": "notification", "email": email, "message": message})
        return True


class StubEmailService:
    """Stub（桩对象）：提供预定义的响应"""

    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.call_count = 0

    def send_welcome_email(self, email):
        """总是返回预定义的结果"""
        self.call_count += 1
        if self.should_fail:
            raise Exception("邮件服务暂时不可用")
        return True


# ==================== 测试类 ====================

class TestUserServiceWithMocks(unittest.TestCase):
    """使用Mock进行测试"""

    def test_register_user_calls_email_service_correctly(self):
        """测试：注册用户时正确调用了邮件服务"""
        # 创建Mock对象作为邮件服务的替代品
        mock_email_service = Mock(spec=EmailService)

        # 配置Mock的行为（可选）
        mock_email_service.send_welcome_email.return_value = True

        # 创建用户服务实例，注入Mock
        user_service = UserService(mock_email_service)

        # 执行被测试的方法
        result = user_service.register_user("张三", "zhangsan@example.com")

        # 验证结果
        self.assertEqual(result["username"], "张三")
        self.assertEqual(result["email"], "zhangsan@example.com")
        self.assertEqual(result["status"], "active")

        # 验证Mock被正确调用
        mock_email_service.send_welcome_email.assert_called_once_with("zhangsan@example.com")

        # 验证没有调用其他方法
        mock_email_service.send_notification.assert_not_called()

    def test_register_user_handles_email_service_failure(self):
        """测试：处理邮件服务失败的情况"""
        # 创建会抛出异常的Mock
        mock_email_service = Mock(spec=EmailService)
        mock_email_service.send_welcome_email.side_effect = Exception("网络错误")

        user_service = UserService(mock_email_service)

        # 即使邮件服务失败，用户仍然应该被创建
        result = user_service.register_user("李四", "lisi@example.com")

        self.assertEqual(result["username"], "李四")
        # 注意：在这个简单实现中，我们不处理邮件发送失败的情况
        # 在实际项目中，你可能需要添加异常处理逻辑


class TestUserServiceWithStubs(unittest.TestCase):
    """使用Stub进行测试"""

    def test_register_user_with_successful_stub(self):
        """测试：使用成功的Stub"""
        stub_email_service = StubEmailService(should_fail=False)
        user_service = UserService(stub_email_service)

        result = user_service.register_user("王五", "wangwu@example.com")

        self.assertEqual(result["username"], "王五")
        self.assertEqual(stub_email_service.call_count, 1)

    def test_register_user_with_failing_stub(self):
        """测试：使用失败的Stub"""
        stub_email_service = StubEmailService(should_fail=True)
        user_service = UserService(stub_email_service)

        # 当前实现不会处理邮件发送失败，所以不会抛出异常
        result = user_service.register_user("赵六", "zhaoliu@example.com")
        self.assertEqual(result["username"], "赵六")


class TestUserServiceWithFakes(unittest.TestCase):
    """使用Fake进行测试"""

    def test_register_user_with_fake_email_service(self):
        """测试：使用Fake邮件服务"""
        fake_email_service = FakeEmailService()
        user_service = UserService(fake_email_service)

        result = user_service.register_user("孙七", "sunqi@example.com")

        # 验证用户创建成功
        self.assertEqual(result["username"], "孙七")

        # 验证Fake记录了邮件发送
        self.assertEqual(len(fake_email_service.sent_emails), 1)
        self.assertEqual(fake_email_service.sent_emails[0]["type"], "welcome")
        self.assertEqual(fake_email_service.sent_emails[0]["email"], "sunqi@example.com")


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)