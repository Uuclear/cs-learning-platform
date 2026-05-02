#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 哈希函数应用演示

本示例展示了：
1. 不同哈希算法的使用（MD5, SHA-1, SHA-256, SHA-3）
2. 密码哈希的最佳实践
3. 数字签名的基本原理
"""

import hashlib
import hmac
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def compare_hash_algorithms():
    """比较不同哈希算法"""
    print("=== 哈希算法比较 ===")

    message = "网络安全课程示例消息".encode("utf-8")
    algorithms = ['md5', 'sha1', 'sha256', 'sha3_256']

    for algo in algorithms:
        if algo == 'md5':
            hash_obj = hashlib.md5()
        elif algo == 'sha1':
            hash_obj = hashlib.sha1()
        elif algo == 'sha256':
            hash_obj = hashlib.sha256()
        elif algo == 'sha3_256':
            hash_obj = hashlib.sha3_256()
        else:
            continue

        hash_obj.update(message)
        digest = hash_obj.hexdigest()
        print(f"{algo.upper()}: {digest[:32]}... ({len(digest)*4} bits)")

    # 安全性说明
    print("\n⚠️  安全性说明:")
    print("- MD5 和 SHA-1 已被证明不安全，不应在新项目中使用")
    print("- SHA-256 和 SHA-3 是当前推荐的安全哈希算法")


def password_hashing_demo():
    """密码哈希演示 - 使用加盐哈希"""
    print("\n=== 密码哈希最佳实践 ===")

    password = "my_secure_password_123"
    print(f"原始密码: {password}")

    # 方法1: 简单哈希（不安全！）
    simple_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"简单SHA-256哈希: {simple_hash}")

    # 方法2: 加盐哈希（推荐）
    salt = secrets.token_hex(32)  # 生成随机盐值
    salted_password = password + salt
    secure_hash = hashlib.sha256(salted_password.encode()).hexdigest()
    print(f"加盐SHA-256哈希: {secure_hash}")
    print(f"使用的盐值: {salt}")

    # 验证密码
    def verify_password(input_password, stored_hash, stored_salt):
        test_salted = input_password + stored_salt
        test_hash = hashlib.sha256(test_salted.encode()).hexdigest()
        return test_hash == stored_hash

    # 测试正确密码
    is_valid = verify_password("my_secure_password_123", secure_hash, salt)
    print(f"验证正确密码: {'✅' if is_valid else '❌'}")

    # 测试错误密码
    is_valid = verify_password("wrong_password", secure_hash, salt)
    print(f"验证错误密码: {'✅' if is_valid else '❌'}")

    # ⚠️ 注意：实际应用中应使用专门的密码哈希函数如 bcrypt, scrypt, Argon2
    print("\n⚠️  重要提示: 实际应用中应使用 bcrypt/scrypt/Argon2 等专用密码哈希函数")


def digital_signature_demo():
    """数字签名演示"""
    print("\n=== 数字签名演示 ===")

    try:
        # 生成密钥对
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # 要签名的消息
        message = "这是需要签名的重要消息".encode("utf-8")

        # 创建数字签名
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print(f"原始消息: {message.decode('utf-8')}")
        print(f"数字签名: {signature[:20].hex()}...")

        # 验证签名
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("✅ 数字签名验证成功！消息未被篡改")
        except Exception as e:
            print(f"❌ 数字签名验证失败: {e}")

        # 尝试验证被篡改的消息
        tampered_message = "这是被篡改的消息".encode("utf-8")
        try:
            public_key.verify(
                signature,
                tampered_message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print("❌ 篡改的消息验证成功！这不应该发生")
        except Exception:
            print("✅ 篡改的消息验证失败！数字签名有效保护了消息完整性")

    except ImportError:
        print("需要安装 cryptography 库进行数字签名演示")
        print("pip install cryptography")


def hmac_demo():
    """HMAC (基于哈希的消息认证码) 演示"""
    print("\n=== HMAC 演示 ===")

    message = "需要认证的消息".encode("utf-8")
    key = secrets.token_bytes(32)  # 32字节密钥

    # 创建HMAC
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    hmac_digest = hmac_obj.hexdigest()

    print(f"原始消息: {message.decode('utf-8')}")
    print(f"HMAC: {hmac_digest}")

    # 验证HMAC
    def verify_hmac(input_message, input_hmac, input_key):
        expected_hmac = hmac.new(input_key, input_message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_hmac, input_hmac)

    # 验证正确消息
    is_valid = verify_hmac(message, hmac_digest, key)
    print(f"验证正确消息: {'✅' if is_valid else '❌'}")

    # 验证篡改消息
    tampered_message = "篡改的消息".encode("utf-8")
    is_valid = verify_hmac(tampered_message, hmac_digest, key)
    print(f"验证篡改消息: {'✅' if is_valid else '❌'}")


if __name__ == "__main__":
    compare_hash_algorithms()
    password_hashing_demo()
    digital_signature_demo()
    hmac_demo()