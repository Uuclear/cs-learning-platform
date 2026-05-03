#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: 安全密码存储系统
使用PBKDF2概念实现安全的密码存储和验证
"""

import hashlib
import secrets
import base64
from typing import Tuple


def generate_salt(length: int = 32) -> bytes:
    """生成密码学安全的随机盐值"""
    return secrets.token_bytes(length)


def pbkdf2_hash(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """
    PBKDF2哈希函数模拟
    实际应用中应使用hashlib.pbkdf2_hmac()
    """
    # 使用多次哈希来增加计算成本
    current = (password.encode() + salt)
    for _ in range(iterations):
        current = hashlib.sha256(current).digest()
    return current


def create_password_hash(password: str) -> str:
    """
    创建密码哈希用于存储
    返回格式: iterations$salt$hash
    """
    salt = generate_salt()
    iterations = 100000  # 足够高的迭代次数

    password_hash = pbkdf2_hash(password, salt, iterations)

    # 编码为字符串存储
    salt_b64 = base64.b64encode(salt).decode('ascii')
    hash_b64 = base64.b64encode(password_hash).decode('ascii')

    return f"{iterations}${salt_b64}${hash_b64}"


def verify_password(password: str, stored_hash: str) -> bool:
    """
    验证密码是否正确
    """
    try:
        iterations_str, salt_b64, hash_b64 = stored_hash.split('$')
        iterations = int(iterations_str)
        salt = base64.b64decode(salt_b64)
        stored_hash_bytes = base64.b64decode(hash_b64)

        # 使用相同的参数重新计算哈希
        test_hash = pbkdf2_hash(password, salt, iterations)

        # 比较哈希值（使用恒定时间比较防止时序攻击）
        return hmac_compare(test_hash, stored_hash_bytes)
    except Exception as e:
        print(f"密码验证错误: {e}")
        return False


def hmac_compare(a: bytes, b: bytes) -> bool:
    """
    恒定时间比较，防止时序攻击
    """
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


class SecurePasswordStorage:
    """安全密码存储系统类"""

    def __init__(self):
        self.users = {}

    def register_user(self, username: str, password: str) -> bool:
        """注册新用户"""
        if username in self.users:
            print(f"❌ 用户 {username} 已存在")
            return False

        if len(password) < 8:
            print("❌ 密码长度至少8位")
            return False

        # 创建密码哈希
        password_hash = create_password_hash(password)
        self.users[username] = password_hash
        print(f"✅ 用户 {username} 注册成功")
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """用户认证"""
        if username not in self.users:
            print(f"❌ 用户 {username} 不存在")
            return False

        stored_hash = self.users[username]
        if verify_password(password, stored_hash):
            print(f"✅ 用户 {username} 认证成功")
            return True
        else:
            print(f"❌ 密码错误")
            return False

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """更改密码"""
        if not self.authenticate_user(username, old_password):
            return False

        if len(new_password) < 8:
            print("❌ 新密码长度至少8位")
            return False

        new_hash = create_password_hash(new_password)
        self.users[username] = new_hash
        print(f"✅ 用户 {username} 密码已更新")
        return True


def main():
    print("🔐 安全密码存储系统演示")
    print("=" * 50)

    # 创建密码存储系统
    storage = SecurePasswordStorage()

    # 注册用户
    print("\n=== 用户注册 ===")
    storage.register_user("alice", "my_secure_password_123")
    storage.register_user("bob", "another_strong_password")
    storage.register_user("charlie", "short")  # 太短，应该失败

    # 用户认证
    print("\n=== 用户认证 ===")
    storage.authenticate_user("alice", "my_secure_password_123")  # 应该成功
    storage.authenticate_user("alice", "wrong_password")         # 应该失败
    storage.authenticate_user("dave", "any_password")           # 用户不存在

    # 更改密码
    print("\n=== 更改密码 ===")
    storage.change_password("alice", "my_secure_password_123", "new_secure_password_456")
    storage.authenticate_user("alice", "new_secure_password_456")  # 应该成功

    # 查看存储的哈希格式
    print(f"\n存储的哈希示例: {storage.users['alice'][:50]}...")
    print("格式: iterations$salt$hash")

    print("\n💡 关键特性:")
    print("- 使用随机盐值防止彩虹表攻击")
    print("- 高迭代次数抵抗暴力破解")
    print("- 恒定时间比较防止时序攻击")
    print("- 密码策略强制执行")


if __name__ == "__main__":
    main()