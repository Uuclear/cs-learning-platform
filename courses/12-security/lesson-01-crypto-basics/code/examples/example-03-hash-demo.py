#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 哈希函数演示
展示SHA-256哈希、碰撞抵抗性和密码哈希
"""

import hashlib
import secrets
import time
from typing import Tuple


def demonstrate_basic_hash():
    """基本哈希函数演示"""
    print("=== 基本哈希函数特性 ===")

    # 相同输入产生相同输出
    message1 = "Hello, World!"
    hash1 = hashlib.sha256(message1.encode()).hexdigest()
    hash2 = hashlib.sha256(message1.encode()).hexdigest()
    print(f"消息: {message1}")
    print(f"哈希1: {hash1[:32]}...")
    print(f"哈希2: {hash2[:32]}...")
    print(f"相同输入产生相同输出: {hash1 == hash2}")

    # 微小变化产生完全不同输出（雪崩效应）
    message2 = "Hello, World?"  # 只改变一个字符
    hash3 = hashlib.sha256(message2.encode()).hexdigest()
    print(f"\n微小变化的消息: {message2}")
    print(f"哈希3: {hash3[:32]}...")

    # 比较两个哈希的差异
    diff_bits = sum(bin(int(hash1[i], 16) ^ int(hash3[i], 16)).count('1')
                    for i in range(len(hash1)))
    print(f"哈希1和哈希3不同的位数: {diff_bits} / {len(hash1)*4}")


def demonstrate_collision_resistance():
    """碰撞抵抗性演示（概念性）"""
    print("\n=== 碰撞抵抗性 ===")
    print("理论上，找到两个不同输入产生相同SHA-256哈希值需要:")
    print("- 穷举搜索: 2^256 ≈ 1.16×10^77 次尝试")
    print("- 即使每秒尝试10亿次，也需要约 3.7×10^60 年")
    print("- 宇宙年龄约为 1.38×10^10 年")
    print("因此，SHA-256被认为是碰撞抵抗的。")


def password_hashing_demo():
    """密码哈希演示"""
    print("\n=== 密码哈希最佳实践 ===")

    password = "my_secure_password_123"
    print(f"原始密码: {password}")

    # ❌ 错误做法：直接哈希密码
    bad_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"❌ 直接哈希: {bad_hash[:32]}...")
    print("  问题: 相同密码总是产生相同哈希，容易被彩虹表攻击")

    # ✅ 正确做法：使用随机盐值
    salt = secrets.token_hex(32)  # 32字节随机盐值
    salted_password = password + salt
    good_hash = hashlib.sha256(salted_password.encode()).hexdigest()
    print(f"\n✅ 加盐哈希:")
    print(f"  盐值: {salt[:32]}...")
    print(f"  哈希: {good_hash[:32]}...")
    print("  优势: 即使密码相同，每次哈希结果都不同")

    # ✅ 更好的做法：使用专门的密码哈希函数（如PBKDF2）
    # 这里用多次哈希模拟慢哈希的概念
    def slow_hash(password: str, salt: str, iterations: int = 100000) -> str:
        """模拟慢哈希函数"""
        current = (password + salt).encode()
        for _ in range(iterations):
            current = hashlib.sha256(current).digest()
        return current.hex()

    start_time = time.time()
    pbkdf2_sim_hash = slow_hash(password, salt, 10000)  # 减少迭代次数以便演示
    end_time = time.time()

    print(f"\n✅ 慢哈希 (模拟PBKDF2):")
    print(f"  哈希: {pbkdf2_sim_hash[:32]}...")
    print(f"  计算时间: {(end_time - start_time)*1000:.2f} ms")
    print("  优势: 抵抗暴力破解，因为计算成本高")


def hash_verification_demo():
    """哈希验证演示"""
    print("\n=== 数据完整性验证 ===")

    original_data = "重要文件内容：机密项目计划书"
    original_hash = hashlib.sha256(original_data.encode()).hexdigest()

    print(f"原始数据: {original_data}")
    print(f"原始哈希: {original_hash[:32]}...")

    # 模拟数据被篡改
    tampered_data = "重要文件内容：机密项目计划书（已被修改）"
    tampered_hash = hashlib.sha256(tampered_data.encode()).hexdigest()

    print(f"\n篡改数据: {tampered_data}")
    print(f"篡改哈希: {tampered_hash[:32]}...")
    print(f"数据是否完整: {original_hash == tampered_hash}")


def main():
    print("🔐 哈希函数实战演示")
    print("=" * 50)

    demonstrate_basic_hash()
    demonstrate_collision_resistance()
    password_hashing_demo()
    hash_verification_demo()

    print("\n💡 关键要点:")
    print("- 哈希函数是单向的，无法从哈希值恢复原始数据")
    print("- SHA-256等现代哈希函数具有强碰撞抵抗性")
    print("- 密码存储必须使用加盐和慢哈希")
    print("- 哈希可用于验证数据完整性")


if __name__ == "__main__":
    main()