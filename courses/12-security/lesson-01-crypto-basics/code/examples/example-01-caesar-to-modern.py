#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 从凯撒密码到现代加密
演示密码学的演进和为什么简单密码容易被破解
"""

import string
import collections
from typing import Dict, List


def caesar_cipher(text: str, shift: int) -> str:
    """凯撒密码加密/解密函数"""
    # 创建字母映射表
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return text.upper().translate(table)


def frequency_analysis(ciphertext: str) -> Dict[str, float]:
    """频率分析：计算每个字母在密文中的出现频率"""
    # 只统计字母
    letters_only = ''.join(filter(str.isalpha, ciphertext.upper()))
    total_letters = len(letters_only)

    if total_letters == 0:
        return {}

    # 统计频率
    freq_counter = collections.Counter(letters_only)
    frequencies = {char: count/total_letters * 100
                   for char, count in freq_counter.items()}

    return dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))


def break_caesar_simple(ciphertext: str) -> List[str]:
    """简单的凯撒密码破解：尝试所有可能的偏移量"""
    possible_decryptions = []
    for shift in range(26):
        decrypted = caesar_cipher(ciphertext, -shift)
        possible_decryptions.append(f"偏移{shift:2d}: {decrypted}")
    return possible_decryptions


def modern_encryption_demo():
    """现代加密的安全性演示（使用哈希作为简单示例）"""
    import hashlib
    import secrets

    # 现代加密的关键特性：相同的输入产生完全不同的输出（由于随机盐值）
    message = "Hello, World!"
    print(f"\n=== 现代加密 vs 凯撒密码 ===")
    print(f"原始消息: {message}")

    # 凯撒密码：相同消息总是产生相同密文
    caesar_result = caesar_cipher(message, 3)
    print(f"凯撒密码(偏移3): {caesar_result}")

    # 现代方法：每次加密都不同（这里用带盐的哈希模拟）
    salt1 = secrets.token_hex(16)
    salt2 = secrets.token_hex(16)
    hash1 = hashlib.sha256((message + salt1).encode()).hexdigest()[:32]
    hash2 = hashlib.sha256((message + salt2).encode()).hexdigest()[:32]
    print(f"现代哈希1: {hash1}")
    print(f"现代哈希2: {hash2}")
    print("注意：即使是相同的消息，现代加密也会产生完全不同的输出！")


def main():
    print("🔐 密码学演进演示：从凯撒密码到现代加密")
    print("=" * 60)

    # 原始消息
    original_message = "ATTACK AT DAWN"
    print(f"原始消息: {original_message}")

    # 凯撒加密
    encrypted = caesar_cipher(original_message, 3)
    print(f"凯撒加密(偏移3): {encrypted}")

    # 凯撒解密
    decrypted = caesar_cipher(encrypted, -3)
    print(f"凯撒解密: {decrypted}")

    print("\n=== 频率分析攻击演示 ===")
    # 更长的密文用于频率分析
    long_message = """
    THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.
    THIS SENTENCE CONTAINS EVERY LETTER OF THE ALPHABET.
    CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES
    FOR SECURE COMMUNICATION IN THE PRESENCE OF ADVERSARIES.
    """
    encrypted_long = caesar_cipher(long_message, 7)
    print(f"长文本凯撒加密结果:\n{encrypted_long[:100]}...")

    # 执行频率分析
    frequencies = frequency_analysis(encrypted_long)
    print("\n密文字母频率 (前10个):")
    for i, (char, freq) in enumerate(list(frequencies.items())[:10]):
        print(f"  {char}: {freq:.2f}%")

    print("\n=== 简单破解尝试 ===")
    # 尝试破解短密文
    short_ciphertext = "KHOOR ZRUOG"  # "HELLO WORLD" with shift 3
    print(f"待破解密文: {short_ciphertext}")
    print("所有可能的解密结果:")
    decryptions = break_caesar_simple(short_ciphertext)
    for decryption in decryptions[:5]:  # 只显示前5个
        print(f"  {decryption}")

    # 现代加密对比
    modern_encryption_demo()


if __name__ == "__main__":
    main()