#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: 文件加密工具
使用AES-GCM模式实现文件的加密和解密
"""

import os
import sys
import hashlib
import secrets
from typing import Tuple, Optional


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """从密码派生加密密钥（使用PBKDF2概念）"""
    # 实际应用中应使用专门的密钥派生函数如PBKDF2或scrypt
    key_material = (password.encode() + salt)
    for _ in range(100000):  # 高迭代次数增加计算成本
        key_material = hashlib.sha256(key_material).digest()
    return key_material[:32]  # AES-256需要32字节密钥


def encrypt_file_gcm(input_filename: str, output_filename: str, password: str) -> bool:
    """
    使用AES-GCM模式加密文件
    由于我们没有cryptography库，这里用简化模拟展示概念
    """
    try:
        # 读取输入文件
        with open(input_filename, 'rb') as f:
            plaintext = f.read()

        print(f"正在加密文件: {input_filename} ({len(plaintext)} 字节)")

        # 生成随机盐值和nonce（GCM需要）
        salt = secrets.token_bytes(16)
        nonce = secrets.token_bytes(12)  # GCM推荐12字节nonce

        # 从密码派生密钥
        key = derive_key_from_password(password, salt)

        # 简化的GCM加密模拟（实际应使用真正的AES-GCM）
        # 这里只演示概念：加密 + 认证标签
        import hashlib

        # 简单的流加密模拟（不安全！仅用于教学）
        encrypted_data = bytearray()
        for i, byte in enumerate(plaintext):
            # 使用密钥和nonce生成伪随机流
            stream_key = hashlib.sha256(key + nonce + i.to_bytes(8, 'big')).digest()
            encrypted_data.append(byte ^ stream_key[i % len(stream_key)])

        # 生成认证标签（GCM提供完整性保护）
        auth_data = salt + nonce + bytes(encrypted_data)
        auth_tag = hashlib.sha256(auth_data).digest()[:16]  # 16字节标签

        # 写入输出文件：salt + nonce + auth_tag + encrypted_data
        with open(output_filename, 'wb') as f:
            f.write(salt)
            f.write(nonce)
            f.write(auth_tag)
            f.write(encrypted_data)

        print(f"✅ 文件已加密到: {output_filename}")
        return True

    except Exception as e:
        print(f"❌ 加密失败: {e}")
        return False


def decrypt_file_gcm(input_filename: str, output_filename: str, password: str) -> bool:
    """
    使用AES-GCM模式解密文件
    """
    try:
        # 读取加密文件
        with open(input_filename, 'rb') as f:
            file_data = f.read()

        if len(file_data) < 44:  # 最小长度：16(salt)+12(nonce)+16(tag)
            print("❌ 文件太小，不是有效的加密文件")
            return False

        # 提取头部信息
        salt = file_data[:16]
        nonce = file_data[16:28]
        auth_tag = file_data[28:44]
        encrypted_data = file_data[44:]

        print(f"正在解密文件: {input_filename} ({len(encrypted_data)} 字节)")

        # 从密码派生密钥
        key = derive_key_from_password(password, salt)

        # 验证认证标签（完整性检查）
        expected_auth_data = salt + nonce + encrypted_data
        expected_auth_tag = hashlib.sha256(expected_auth_data).digest()[:16]

        if expected_auth_tag != auth_tag:
            print("❌ 认证失败！文件可能已被篡改")
            return False

        # 解密数据（与加密过程相同，因为是XOR）
        decrypted_data = bytearray()
        for i, byte in enumerate(encrypted_data):
            stream_key = hashlib.sha256(key + nonce + i.to_bytes(8, 'big')).digest()
            decrypted_data.append(byte ^ stream_key[i % len(stream_key)])

        # 写入解密后的文件
        with open(output_filename, 'wb') as f:
            f.write(decrypted_data)

        print(f"✅ 文件已解密到: {output_filename}")
        return True

    except Exception as e:
        print(f"❌ 解密失败: {e}")
        return False


def main():
    if len(sys.argv) != 5:
        print("用法:")
        print(f"  {sys.argv[0]} encrypt <输入文件> <输出文件> <密码>")
        print(f"  {sys.argv[0]} decrypt <输入文件> <输出文件> <密码>")
        print("\n注意: 这是一个概念演示，实际应用应使用真正的AES-GCM实现")
        return

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    password = sys.argv[4]

    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return

    if operation == "encrypt":
        success = encrypt_file_gcm(input_file, output_file, password)
    elif operation == "decrypt":
        success = decrypt_file_gcm(input_file, output_file, password)
    else:
        print(f"❌ 未知操作: {operation}")
        return

    if success:
        print("✅ 操作完成")
    else:
        print("❌ 操作失败")


def demo():
    """演示函数（当直接运行时）"""
    print("🔐 文件加密工具演示")
    print("=" * 50)

    # 创建测试文件
    test_content = b"This is a secret test file for encryption demonstration!"
    with open("test_plaintext.txt", "wb") as f:
        f.write(test_content)

    print("创建测试文件: test_plaintext.txt")

    # 加密
    encrypt_file_gcm("test_plaintext.txt", "test_encrypted.bin", "my_secret_password")

    # 解密
    decrypt_file_gcm("test_encrypted.bin", "test_decrypted.txt", "my_secret_password")

    # 验证
    with open("test_decrypted.txt", "rb") as f:
        decrypted_content = f.read()

    print(f"原始内容匹配: {test_content == decrypted_content}")

    # 清理测试文件
    for filename in ["test_plaintext.txt", "test_encrypted.bin", "test_decrypted.txt"]:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"清理: {filename}")

    print("\n💡 注意:")
    print("- 这是AES-GCM概念的简化演示")
    print("- 实际应用应使用cryptography等专业库")
    print("- GCM模式同时提供机密性和完整性保护")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        demo()
    else:
        main()