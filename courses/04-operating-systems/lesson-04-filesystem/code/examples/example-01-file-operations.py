#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 基本文件操作演示
展示文件的创建、读取、写入、获取元数据和删除操作
"""

import os
import stat
from datetime import datetime

def demonstrate_file_operations():
    """演示基本的文件操作"""
    # 创建一个测试文件
    filename = "test_file.txt"

    print("=" * 50)
    print("📁 示例1: 基本文件操作演示")
    print("=" * 50)

    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("这是测试文件的内容！\n")
        f.write("文件系统真神奇！\n")
        f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ 成功创建文件: {filename}")

    # 读取文件
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"\n📄 文件内容:")
        print(content)

    # 获取文件状态信息（类似inode信息）
    file_stat = os.stat(filename)
    print(f"📊 文件统计信息:")
    print(f"   - 文件大小: {file_stat.st_size} 字节")
    print(f"   - 权限模式: {oct(file_stat.st_mode & 0o777)}")  # 只显示权限位
    print(f"   - inode号: {file_stat.st_ino}")
    print(f"   - 硬链接数: {file_stat.st_nlink}")
    print(f"   - 所有者ID: {file_stat.st_uid}")
    print(f"   - 组ID: {file_stat.st_gid}")

    # 显示人类可读的权限
    permissions = stat.filemode(file_stat.st_mode)
    print(f"   - 详细权限: {permissions}")

    # 删除文件
    os.remove(filename)
    print(f"\n🗑️  文件已删除: {filename}")

    # 验证文件确实被删除了
    if not os.path.exists(filename):
        print("✅ 文件删除成功，确认不存在")
    else:
        print("❌ 文件删除失败！")

if __name__ == "__main__":
    demonstrate_file_operations()