#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 目录遍历演示
展示如何递归遍历目录结构，模拟ls -R命令的功能
"""

import os
import sys

def format_size(size_bytes):
    """将字节大小格式化为人类可读的格式"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    if i == 0:
        return f"{int(size_bytes)}{size_names[i]}"
    else:
        return f"{size_bytes:.1f}{size_names[i]}"

def traverse_directory_tree(root_dir=".", max_depth=3):
    """
    递归遍历目录树

    Args:
        root_dir (str): 要遍历的根目录
        max_depth (int): 最大递归深度，防止无限递归
    """
    print("=" * 50)
    print(f"🔍 示例2: 目录遍历演示")
    print(f"根目录: {os.path.abspath(root_dir)}")
    print(f"最大深度: {max_depth}")
    print("=" * 50)

    def _traverse(current_path, depth=0):
        if depth > max_depth:
            indent = "  " * depth
            print(f"{indent}... (深度限制，停止遍历)")
            return

        indent = "  " * depth
        try:
            # 获取目录内容并排序
            items = os.listdir(current_path)
            items.sort()

            for item in items:
                item_path = os.path.join(current_path, item)

                try:
                    if os.path.isdir(item_path):
                        print(f"{indent}📁 {item}/")
                        # 递归遍历子目录
                        _traverse(item_path, depth + 1)
                    else:
                        # 获取文件大小
                        size = os.path.getsize(item_path)
                        size_str = format_size(size)
                        print(f"{indent}📄 {item} ({size_str})")

                except (OSError, PermissionError) as e:
                    print(f"{indent}❌ 无法访问 {item}: {e}")

        except PermissionError:
            print(f"{indent}🔒 权限不足，无法访问 {current_path}")
        except Exception as e:
            print(f"{indent}❌ 错误: {e}")

    # 开始遍历
    _traverse(root_dir)

def main():
    """主函数"""
    # 如果提供了命令行参数，使用第一个参数作为根目录
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = "."

    traverse_directory_tree(root_dir)

if __name__ == "__main__":
    main()