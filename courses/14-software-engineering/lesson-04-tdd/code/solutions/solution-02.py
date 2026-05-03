#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：用户验证器实现

使用TDD方式实现的用户验证器，包含用户名、密码和邮箱验证
"""

import re


class UserValidator:
    """用户验证器类"""

    def validate_username(self, username):
        """
        验证用户名

        Args:
            username (str): 用户名

        Returns:
            bool: 用户名是否有效

        规则：
            - 长度必须在3-20个字符之间
            - 只能包含字母、数字、下划线和连字符
        """
        if not isinstance(username, str):
            return False

        if len(username) < 3 or len(username) > 20:
            return False

        # 只允许字母、数字、下划线和连字符
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False

        return True

    def validate_password(self, password):
        """
        验证密码

        Args:
            password (str): 密码

        Returns:
            bool: 密码是否有效

        规则：
            - 长度至少8个字符
            - 必须包含至少一个小写字母
            - 必须包含至少一个大写字母
            - 必须包含至少一个数字
        """
        if not isinstance(password, str):
            return False

        if len(password) < 8:
            return False

        # 检查是否包含小写字母
        if not re.search(r'[a-z]', password):
            return False

        # 检查是否包含大写字母
        if not re.search(r'[A-Z]', password):
            return False

        # 检查是否包含数字
        if not re.search(r'\d', password):
            return False

        return True

    def validate_email(self, email):
        """
        验证邮箱格式

        Args:
            email (str): 邮箱地址

        Returns:
            bool: 邮箱格式是否有效
        """
        if not isinstance(email, str):
            return False

        # 基本的邮箱正则表达式
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_user(self, username, password, email):
        """
        验证完整的用户信息

        Args:
            username (str): 用户名
            password (str): 密码
            email (str): 邮箱

        Returns:
            dict: 验证结果，包含是否成功和错误信息
        """
        errors = []

        if not self.validate_username(username):
            errors.append("用户名无效：长度必须在3-20个字符之间，只能包含字母、数字、下划线和连字符")

        if not self.validate_password(password):
            errors.append("密码无效：长度至少8个字符，必须包含大小写字母和数字")

        if not self.validate_email(email):
            errors.append("邮箱格式无效")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


if __name__ == '__main__':
    # 测试用户验证器
    validator = UserValidator()

    # 测试有效的用户信息
    result = validator.validate_user("test_user", "Password123", "test@example.com")
    print("有效用户测试:", result)

    # 测试无效的用户信息
    result = validator.validate_user("ab", "pass", "invalid-email")
    print("无效用户测试:", result)