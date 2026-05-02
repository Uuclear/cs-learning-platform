#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 加密基础 - 对称加密和非对称加密演示

本示例展示了：
1. 对称加密（AES）的基本用法
2. 非对称加密（RSA）的基本用法
3. 两种加密方式的性能对比
"""

import time
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def symmetric_encryption_demo():
    """对称加密演示 - 使用Fernet (基于AES)"""
    print("=== 对称加密演示 ===")

    # 生成密钥
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # 要加密的消息
    message = "这是我的秘密消息！".encode("utf-8")
    print(f"原始消息: {message.decode('utf-8')}")

    # 加密
    encrypted_message = fernet.encrypt(message)
    print(f"加密后: {encrypted_message}")

    # 解密
    decrypted_message = fernet.decrypt(encrypted_message)
    print(f"解密后: {decrypted_message.decode('utf-8')}")

    return key, encrypted_message


def asymmetric_encryption_demo():
    """非对称加密演示 - 使用RSA"""
    print("\n=== 非对称加密演示 ===")

    # 生成密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 要加密的消息
    message = "这是我的秘密消息！".encode("utf-8")
    print(f"原始消息: {message.decode('utf-8')}")

    # 使用公钥加密
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"加密后: {encrypted_message[:20]}...")  # 只显示前20个字节

    # 使用私钥解密
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"解密后: {decrypted_message.decode()}")

    return private_key, public_key, encrypted_message


def performance_comparison():
    """性能对比演示"""
    print("\n=== 性能对比 ===")

    # 对称加密性能测试
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = b"性能测试消息" * 100

    start_time = time.time()
    for _ in range(100):
        encrypted = fernet.encrypt(message)
        decrypted = fernet.decrypt(encrypted)
    symmetric_time = time.time() - start_time

    # 非对称加密性能测试
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    start_time = time.time()
    for _ in range(10):  # 非对称加密较慢，只测试10次
        encrypted = public_key.encrypt(
            message,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None)
        )
        decrypted = private_key.decrypt(
            encrypted,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None)
        )
    asymmetric_time = time.time() - start_time

    print(f"对称加密 (100次): {symmetric_time:.4f} 秒")
    print(f"非对称加密 (10次): {asymmetric_time:.4f} 秒")
    print(f"相对性能: 非对称加密比对称加密慢约 {asymmetric_time/10/(symmetric_time/100):.0f} 倍")


if __name__ == "__main__":
    try:
        symmetric_encryption_demo()
        asymmetric_encryption_demo()
        performance_comparison()
    except ImportError:
        print("需要安装 cryptography 库:")
        print("pip install cryptography")