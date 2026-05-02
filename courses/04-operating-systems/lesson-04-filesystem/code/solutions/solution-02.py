#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 目录大小计算器
计算指定目录的总大小（包括所有子目录和文件）
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
        return f"{size_bytes:.2f}{size_names[i]}"

def calculate_directory_size(directory_path, show_progress=False):
    """
    计算目录总大小

    Args:
        directory_path (str): 目录路径
        show_progress (bool): 是否显示进度信息

    Returns:
        int: 总字节数
    """
    if not os.path.exists(directory_path):
        print(f"❌ 错误: 路径不存在 - {directory_path}")
        return 0

    if not os.path.isdir(directory_path):
        # 如果是文件，直接返回文件大小
        try:
            file_size = os.path.getsize(directory_path)
            if show_progress:
                print(f"📄 {directory_path} -> {format_size(file_size)}")
            return file_size
        except (OSError, PermissionError) as e:
            print(f"❌ 无法获取文件大小 {directory_path}: {e}")
            return 0

    total_size = 0
    processed_count = 0

    try:
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    processed_count += 1

                    if show_progress and processed_count % 100 == 0:
                        print(f"🔄 已处理 {processed_count} 个文件，当前大小: {format_size(total_size)}")

                except (OSError, PermissionError) as e:
                    if show_progress:
                        print(f"⚠️  跳过文件 {file_path}: {e}")
                    continue

    except PermissionError as e:
        print(f"❌ 权限不足，无法遍历目录 {directory_path}: {e}")
        return total_size
    except Exception as e:
        print(f"❌ 遍历目录时发生错误 {directory_path}: {e}")
        return total_size

    if show_progress:
        print(f"✅ 完成！总共处理了 {processed_count} 个文件")

    return total_size

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python solution-2.py <目录路径> [show_progress]")
        print("示例: python solution-2.py /home/user")
        print("      python solution-2.py /home/user True")
        return

    directory_path = sys.argv[1]
    show_progress = len(sys.argv) > 2 and sys.argv[2].lower() == 'true'

    print(f"🔍 计算目录大小: {os.path.abspath(directory_path)}")
    if show_progress:
        print("📊 显示进度信息...")

    total_size = calculate_directory_size(directory_path, show_progress)
    formatted_size = format_size(total_size)

    print(f"\n📈 目录总大小: {formatted_size} ({total_size} 字节)")

if __name__ == "__main__":
    main()