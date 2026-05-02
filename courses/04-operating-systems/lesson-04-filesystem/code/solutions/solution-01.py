#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 文件信息查看器
显示指定文件或目录的详细信息
"""

import os
import stat
import sys
from datetime import datetime

def format_permissions(mode):
    """将权限模式转换为人类可读的字符串"""
    return stat.filemode(mode)

def format_timestamp(timestamp):
    """将时间戳格式化为可读日期"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_file_info(path):
    """获取并显示文件/目录的详细信息"""
    if not os.path.exists(path):
        print(f"❌ 错误: 路径不存在 - {path}")
        return False

    try:
        # 获取文件状态
        file_stat = os.stat(path)

        print("=" * 60)
        print(f"📄 文件信息: {os.path.abspath(path)}")
        print("=" * 60)

        # 基本信息
        print(f"类型: {'目录' if os.path.isdir(path) else '文件'}")
        print(f"大小: {file_stat.st_size} 字节")
        print(f"inode号: {file_stat.st_ino}")
        print(f"硬链接数: {file_stat.st_nlink}")

        # 权限信息
        permissions = format_permissions(file_stat.st_mode)
        print(f"权限: {permissions} ({oct(file_stat.st_mode & 0o777)})")

        # 所有者信息（在Unix系统上）
        print(f"所有者ID: {file_stat.st_uid}")
        print(f"组ID: {file_stat.st_gid}")

        # 时间信息
        print(f"创建时间: {format_timestamp(file_stat.st_ctime)}")
        print(f"修改时间: {format_timestamp(file_stat.st_mtime)}")
        print(f"访问时间: {format_timestamp(file_stat.st_atime)}")

        return True

    except PermissionError:
        print(f"❌ 权限不足: 无法访问 {path}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: python solution-01.py <文件路径>")
        print("示例: python solution-01.py /etc/passwd")
        return

    path = sys.argv[1]
    get_file_info(path)

if __name__ == "__main__":
    main()