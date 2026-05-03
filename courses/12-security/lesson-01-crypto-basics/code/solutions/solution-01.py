#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: XOR密码与频率分析攻击
实现简单的XOR密码，并演示如何通过频率分析破解它
"""

import string
import collections
from typing import List


def xor_cipher(text: str, key: str) -> str:
    """XOR密码加密/解密（使用重复密钥）"""
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            # 只对字母进行XOR操作，保持大小写
            is_upper = char.isupper()
            char_lower = char.lower()
            key_char = key[key_index % len(key)].lower()

            # 将字母转换为0-25的数字，进行XOR，再转回字母
            char_num = ord(char_lower) - ord('a')
            key_num = ord(key_char) - ord('a')
            xor_result = (char_num ^ key_num) % 26
            result_char = chr(xor_result + ord('a'))

            if is_upper:
                result_char = result_char.upper()
            result.append(result_char)
            key_index += 1
        else:
            # 非字母字符保持不变
            result.append(char)

    return ''.join(result)


def frequency_analysis_attack(ciphertext: str, max_key_length: int = 10) -> List[str]:
    """
    频率分析攻击XOR密码
    假设密钥长度在1到max_key_length之间
    """
    # 英文字符频率（按常见程度排序）
    english_freq = "ETAOINSHRDLUCMFWYPVBGKJQXZ"

    possible_decryptions = []

    # 尝试不同的密钥长度
    for key_len in range(1, min(max_key_length + 1, len(ciphertext))):
        # 将密文按密钥长度分组
        groups = [''] * key_len
        letter_positions = []  # 记录哪些位置是字母

        for i, char in enumerate(ciphertext):
            if char.isalpha():
                groups[i % key_len] += char
                letter_positions.append(i)

        # 对每个组进行频率分析，猜测密钥字符
        guessed_key = []
        for group in groups:
            if not group:
                guessed_key.append('a')  # 默认
                continue

            # 统计组内字符频率
            freq_counter = collections.Counter(group.upper())
            most_common_char = freq_counter.most_common(1)[0][0]

            # 假设最常见的字符对应'E'
            e_pos = ord('E') - ord('A')
            common_pos = ord(most_common_char) - ord('A')
            # 计算密钥偏移：common = original ^ key => key = common ^ original
            # 这里简化处理，假设original是'E'
            key_char_pos = (common_pos ^ e_pos) % 26
            key_char = chr(key_char_pos + ord('a'))
            guessed_key.append(key_char)

        guessed_key_str = ''.join(guessed_key)
        decrypted = xor_cipher(ciphertext, guessed_key_str)
        possible_decryptions.append(f"密钥长度{key_len}: '{guessed_key_str}' -> {decrypted[:50]}...")

    return possible_decryptions


def main():
    print("🔐 XOR密码与频率分析攻击")
    print("=" * 50)

    # 原始消息
    original_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. CRYPTOGRAPHY IS FASCINATING!"
    key = "SECRET"

    print(f"原始消息: {original_message}")
    print(f"密钥: {key}")

    # 加密
    encrypted = xor_cipher(original_message, key)
    print(f"XOR加密后: {encrypted}")

    # 解密验证
    decrypted = xor_cipher(encrypted, key)
    print(f"XOR解密后: {decrypted}")
    print(f"解密正确: {original_message == decrypted}")

    print("\n=== 频率分析攻击演示 ===")
    # 使用更长的文本进行攻击演示
    long_message = """
    CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES FOR SECURE COMMUNICATION
    IN THE PRESENCE OF THIRD PARTIES CALLED ADVERSARIES. MODERN CRYPTOGRAPHY EXISTS
    AT THE INTERSECTION OF THE DISCIPLINES OF MATHEMATICS COMPUTER SCIENCE AND
    ELECTRICAL ENGINEERING. CRYPTOGRAPHY PRIOR TO THE MODERN AGE WAS EFFECTIVELY
    SYNONYMOUS WITH ENCRYPTION THE CONVERSION OF INFORMATION FROM A READABLE STATE
    TO APPARENT NONSENSE.
    """
    long_encrypted = xor_cipher(long_message.strip(), "KEY")
    print(f"长文本XOR加密结果:\n{long_encrypted[:100]}...")

    # 执行频率分析攻击
    print("\n尝试通过频率分析破解...")
    attacks = frequency_analysis_attack(long_encrypted, 5)
    for attack in attacks[:3]:  # 显示前3个猜测
        print(f"  {attack}")

    print("\n💡 教训:")
    print("- 简单的重复密钥XOR容易受到频率分析攻击")
    print("- 真正的安全加密需要随机密钥和适当的模式")
    print("- 密钥应该与明文一样长（一次性密码本）才能完全安全")


if __name__ == "__main__":
    main()