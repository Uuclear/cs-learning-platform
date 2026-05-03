#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 对称加密实战
使用Python的cryptography库实现AES加密/解密
如果cryptography库不可用，则使用hashlib进行概念演示
"""

import os
import base64
from typing import Tuple, Optional


def try_modern_crypto() -> bool:
    """尝试导入现代加密库"""
    try:
        from cryptography.fernet import Fernet
        return True
    except ImportError:
        return False


def aes_encryption_modern(message: bytes, key: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """使用cryptography库的现代AES加密"""
    from cryptography.fernet import Fernet

    if key is None:
        key = Fernet.generate_key()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(message)
    return encrypted, key


def aes_decryption_modern(encrypted_data: bytes, key: bytes) -> bytes:
    """使用cryptography库的现代AES解密"""
    from cryptography.fernet import Fernet
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data)
    return decrypted


def simple_aes_simulation(message: str, key: str) -> str:
    """
    简单的AES概念模拟（仅用于教学演示，不安全！）
    实际应用中绝对不要使用这种方法
    """
    # 这只是一个非常简化的模拟，展示对称加密的概念
    # 实际的AES要复杂得多，涉及多轮变换、S盒等
    import hashlib

    # 使用密钥生成一个固定的"加密密钥"
    key_hash = hashlib.sha256(key.encode()).digest()

    # 简单的XOR加密模拟（不安全！）
    message_bytes = message.encode()
    encrypted_bytes = bytearray()
    for i, byte in enumerate(message_bytes):
        encrypted_bytes.append(byte ^ key_hash[i % len(key_hash)])

    return base64.b64encode(encrypted_bytes).decode()


def simple_aes_decryption_simulation(encrypted_b64: str, key: str) -> str:
    """简单的AES解密模拟"""
    import hashlib

    key_hash = hashlib.sha256(key.encode()).digest()
    encrypted_bytes = base64.b64decode(encrypted_b64.encode())

    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        decrypted_bytes.append(byte ^ key_hash[i % len(key_hash)])

    return decrypted_bytes.decode()


def demonstrate_encryption_modes():
    """演示不同的加密模式概念"""
    print("\n=== 加密模式概念演示 ===")
    print("ECB模式: 相同的明文块 → 相同的密文块 (不安全)")
    print("CBC模式: 每个块与前一个密文块异或 (更安全)")
    print("GCM模式: 提供加密和认证 (推荐)")


def main():
    print("🔐 对称加密实战演示")
    print("=" * 50)

    message = "这是需要加密的机密消息！Secret message that needs encryption!"
    print(f"原始消息: {message}")

    # 首先尝试使用现代加密库
    if try_modern_crypto():
        print("\n✅ 使用现代cryptography库:")
        try:
            encrypted_data, key = aes_encryption_modern(message.encode())
            decrypted_data = aes_decryption_modern(encrypted_data, key)

            print(f"加密后 (base64): {base64.b64encode(encrypted_data).decode()[:60]}...")
            print(f"解密后: {decrypted_data.decode()}")
            print(f"加密成功: {message == decrypted_data.decode()}")

            # 演示密钥的重要性
            wrong_key = os.urandom(32)  # 错误的密钥
            try:
                wrong_decrypted = aes_decryption_modern(encrypted_data, base64.b64encode(wrong_key))
                print("❌ 使用错误密钥竟然解密成功了！这不应该发生。")
            except Exception as e:
                print(f"✅ 使用错误密钥解密失败 (正常行为): {type(e).__name__}")

        except Exception as e:
            print(f"❌ 现代加密库使用出错: {e}")
            print("回退到概念演示...")

    else:
        print("\n⚠️  modern cryptography库未安装，使用概念演示:")
        secret_key = "my_secret_password_123"
        encrypted = simple_aes_simulation(message, secret_key)
        decrypted = simple_aes_decryption_simulation(encrypted, secret_key)

        print(f"加密后: {encrypted[:60]}...")
        print(f"解密后: {decrypted}")
        print(f"解密成功: {message == decrypted}")

    # 演示加密模式
    demonstrate_encryption_modes()

    print("\n💡 注意:")
    print("- 真正的安全加密应该使用经过验证的库如cryptography")
    print("- 不要自己实现加密算法")
    print("- 密钥管理比算法本身更重要")


if __name__ == "__main__":
    main()