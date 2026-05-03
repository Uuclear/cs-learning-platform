#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：密码强度检查器 + 安全令牌生成器

实现密码强度验证和安全的随机令牌生成功能。
"""

import re
import secrets
import string
import hashlib
import hmac
from typing import Tuple, List


class PasswordStrengthChecker:
    """密码强度检查器"""

    def __init__(self):
        # 密码强度要求
        self.min_length = 8
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
        self.max_length = 128  # 防止拒绝服务攻击

    def check_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """
        检查密码强度

        Args:
            password: 要检查的密码

        Returns:
            tuple: (是否通过, 错误信息列表)
        """
        errors = []

        # 检查长度
        if len(password) < self.min_length:
            errors.append(f"密码长度至少需要 {self.min_length} 个字符")

        if len(password) > self.max_length:
            errors.append(f"密码长度不能超过 {self.max_length} 个字符")

        # 检查大写字母
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("密码必须包含至少一个大写字母")

        # 检查小写字母
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("密码必须包含至少一个小写字母")

        # 检查数字
        if self.require_digits and not re.search(r'[0-9]', password):
            errors.append("密码必须包含至少一个数字")

        # 检查特殊字符
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("密码必须包含至少一个特殊字符 (!@#$%^&*(),.?\":{}|<>)")

        # 检查常见弱密码（简化版）
        weak_passwords = ['password', '12345678', 'qwerty', 'admin', 'user']
        if password.lower() in weak_passwords:
            errors.append("密码过于简单，请选择更复杂的密码")

        # 检查重复字符模式
        if re.search(r'(.)\1{2,}', password):
            errors.append("密码不应包含过多重复字符")

        is_strong = len(errors) == 0
        return is_strong, errors

    def get_password_score(self, password: str) -> int:
        """
        计算密码强度分数（0-100）

        Args:
            password: 要评分的密码

        Returns:
            int: 密码强度分数
        """
        score = 0

        # 长度分数
        length_score = min(len(password), 20) * 2  # 最多40分
        score += length_score

        # 字符类型分数
        if re.search(r'[a-z]', password):
            score += 15
        if re.search(r'[A-Z]', password):
            score += 15
        if re.search(r'[0-9]', password):
            score += 15
        if re.search(r'[^a-zA-Z0-9]', password):
            score += 15

        # 多样性奖励
        unique_chars = len(set(password))
        diversity_bonus = min(unique_chars, 10)  # 最多10分
        score += diversity_bonus

        return min(score, 100)


class SecureTokenGenerator:
    """安全令牌生成器"""

    @staticmethod
    def generate_random_token(length: int = 32) -> str:
        """
        生成加密安全的随机令牌

        Args:
            length: 令牌长度（字节）

        Returns:
            str: Base64编码的随机令牌
        """
        # 使用 secrets 模块生成加密安全的随机数
        token_bytes = secrets.token_bytes(length)
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_csrf_token() -> str:
        """生成CSRF令牌"""
        return secrets.token_hex(32)

    @staticmethod
    def generate_session_id() -> str:
        """生成会话ID"""
        return secrets.token_urlsafe(48)

    @staticmethod
    def generate_password_reset_token(user_id: str) -> str:
        """
        生成密码重置令牌

        Args:
            user_id: 用户ID

        Returns:
            str: 密码重置令牌
        """
        # 结合用户ID和时间戳生成唯一令牌
        timestamp = str(secrets.randbelow(1000000))
        combined = f"{user_id}:{timestamp}"
        signature = hmac.new(
            key=secrets.token_bytes(32),
            msg=combined.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        return f"{secrets.token_urlsafe(32)}:{signature[:16]}"


def demonstrate_password_checker():
    """演示密码强度检查器"""
    print("=== 密码强度检查器演示 ===\n")

    checker = PasswordStrengthChecker()
    test_passwords = [
        "123456",           # 弱密码
        "Password123",      # 中等密码
        "MySecureP@ssw0rd!", # 强密码
        "aaaaaaaaaaaaaaa",   # 重复字符
        "Short1!"           # 太短
    ]

    for password in test_passwords:
        is_strong, errors = checker.check_password_strength(password)
        score = checker.get_password_score(password)

        print(f"密码: {password}")
        print(f"强度分数: {score}/100")
        print(f"是否通过: {'是' if is_strong else '否'}")
        if errors:
            print(f"错误信息: {', '.join(errors)}")
        print("-" * 50)


def demonstrate_token_generator():
    """演示安全令牌生成器"""
    print("\n=== 安全令牌生成器演示 ===\n")

    generator = SecureTokenGenerator()

    print("随机令牌:", generator.generate_random_token())
    print("CSRF令牌:", generator.generate_csrf_token())
    print("会话ID:", generator.generate_session_id())
    print("密码重置令牌:", generator.generate_password_reset_token("user123"))


def main():
    """主函数 - 演示密码检查器和令牌生成器"""
    demonstrate_password_checker()
    demonstrate_token_generator()

    print("\n=== 使用建议 ===")
    print("1. 密码存储: 使用 bcrypt、scrypt 或 Argon2 进行哈希")
    print("2. 令牌存储: 将令牌存储在安全的Cookie中（HttpOnly, Secure, SameSite）")
    print("3. 令牌有效期: 设置合理的过期时间")
    print("4. 密码策略: 定期要求用户更新密码")


if __name__ == "__main__":
    main()