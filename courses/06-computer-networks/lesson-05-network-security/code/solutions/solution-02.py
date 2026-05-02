#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 实现简单的文件完整性检查器

要求：
- 计算文件的SHA-256哈希值
- 将哈希值保存到 .sha256 文件中
- 验证文件是否被修改
"""

import hashlib
import os


def calculate_file_hash(filepath):
    """计算文件的SHA-256哈希值"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # 逐块读取文件以处理大文件
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"文件 {filepath} 不存在")
        return None


def save_hash_file(filepath, hash_value):
    """将哈希值保存到 .sha256 文件"""
    hash_filepath = filepath + ".sha256"
    with open(hash_filepath, "w") as f:
        f.write(hash_value)
    print(f"哈希值已保存到: {hash_filepath}")


def verify_file_integrity(filepath):
    """验证文件完整性"""
    hash_filepath = filepath + ".sha256"

    if not os.path.exists(hash_filepath):
        print(f"哈希文件 {hash_filepath} 不存在")
        return False

    # 读取保存的哈希值
    with open(hash_filepath, "r") as f:
        saved_hash = f.read().strip()

    # 计算当前文件哈希值
    current_hash = calculate_file_hash(filepath)

    if current_hash is None:
        return False

    # 比较哈希值
    if saved_hash == current_hash:
        print("✅ 文件完整性验证通过！文件未被修改")
        return True
    else:
        print("❌ 文件完整性验证失败！文件可能已被篡改")
        print(f"保存的哈希: {saved_hash}")
        print(f"当前哈希:   {current_hash}")
        return False


if __name__ == "__main__":
    # 创建测试文件
    test_file = "test_document.txt"
    with open(test_file, "w") as f:
        f.write("这是一个用于测试文件完整性检查的文档。\n")
        f.write("网络安全课程 - 文件完整性保护演示\n")

    # 计算并保存哈希值
    file_hash = calculate_file_hash(test_file)
    if file_hash:
        save_hash_file(test_file, file_hash)

        # 验证完整性（应该通过）
        verify_file_integrity(test_file)

        # 修改文件后再次验证（应该失败）
        with open(test_file, "a") as f:
            f.write("额外添加的内容\n")

        print("\n修改文件后再次验证:")
        verify_file_integrity(test_file)