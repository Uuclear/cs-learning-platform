#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增量加载示例：基于时间戳的增量ETL处理
演示如何只处理自上次运行以来的新数据或更新的数据
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


def load_last_watermark(watermark_file: str) -> str:
    """
    加载上次处理的时间戳（水印）

    Args:
        watermark_file: 水印文件路径

    Returns:
        上次处理的时间戳，如果不存在则返回默认值
    """
    if os.path.exists(watermark_file):
        with open(watermark_file, 'r') as f:
            watermark = f.read().strip()
        print(f"🔍 找到上次水印: {watermark}")
    else:
        # 默认设置为24小时前，确保处理一些历史数据
        default_watermark = (datetime.now() - timedelta(hours=24)).isoformat()
        watermark = default_watermark
        print(f"🆕 首次运行，使用默认水印: {watermark}")

    return watermark


def save_current_watermark(watermark_file: str, current_time: str):
    """
    保存当前处理的时间戳作为新的水印

    Args:
        watermark_file: 水印文件路径
        current_time: 当前时间戳
    """
    with open(watermark_file, 'w') as f:
        f.write(current_time)
    print(f"💾 保存新水印: {current_time}")


def extract_new_data(all_data_file: str, last_watermark: str) -> List[Dict[str, Any]]:
    """
    提取阶段：只提取自上次水印以来的新数据

    Args:
        all_data_file: 包含所有数据的文件
        last_watermark: 上次处理的时间戳

    Returns:
        新数据列表
    """
    print("🔄 提取新数据...")
    last_watermark_dt = datetime.fromisoformat(last_watermark.replace('Z', '+00:00'))

    # 模拟从数据库或API获取数据
    all_records = [
        {'id': '1', 'name': '张三', 'updated_at': '2026-05-01T10:00:00', 'status': 'active'},
        {'id': '2', 'name': '李四', 'updated_at': '2026-05-02T14:30:00', 'status': 'active'},
        {'id': '3', 'name': '王五', 'updated_at': '2026-05-03T09:15:00', 'status': 'inactive'},
        {'id': '4', 'name': '赵六', 'updated_at': '2026-05-03T16:45:00', 'status': 'active'}
    ]

    new_records = []
    for record in all_records:
        record_time = datetime.fromisoformat(record['updated_at'].replace('Z', '+00:00'))
        if record_time > last_watermark_dt:
            new_records.append(record)

    print(f"✅ 找到 {len(new_records)} 条新记录")
    return new_records


def transform_incremental_data(new_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    转换阶段：对增量数据进行处理

    Args:
        new_data: 新数据列表

    Returns:
        转换后的数据列表
    """
    print("🔄 转换增量数据...")

    transformed_data = []
    for record in new_data:
        transformed_record = {
            'user_id': record['id'],
            'username': record['name'],
            'last_updated': record['updated_at'],
            'is_active': record['status'] == 'active',
            'processed_at': datetime.now().isoformat()
        }
        transformed_data.append(transformed_record)

    print(f"✅ 转换完成 {len(transformed_data)} 条记录")
    return transformed_data


def load_incremental_data(transformed_data: List[Dict[str, Any]],
                         target_file: str,
                         last_watermark: str):
    """
    加载阶段：增量加载到目标文件
    这里演示了两种策略：
    1. 追加模式：将新数据追加到现有文件
    2. 更新模式：合并新旧数据（去重）

    Args:
        transformed_data: 转换后的数据
        target_file: 目标文件路径
        last_watermark: 上次水印（用于更新模式）
    """
    print("🔄 执行增量加载...")

    # 策略1：追加模式
    existing_data = []
    if os.path.exists(target_file):
        with open(target_file, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

    # 合并数据（简单追加）
    combined_data = existing_data + transformed_data

    # 去重（基于user_id）
    unique_data = {}
    for record in combined_data:
        unique_data[record['user_id']] = record

    final_data = list(unique_data.values())

    # 保存结果
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 增量加载完成，总记录数: {len(final_data)}")


def main():
    """主函数：执行增量ETL流程"""
    print("🚀 启动增量ETL管道")
    print("=" * 50)

    watermark_file = 'last_processed_watermark.txt'
    target_file = 'users_incremental.json'

    # 1. 获取上次处理的水印
    last_watermark = load_last_watermark(watermark_file)

    # 2. 提取新数据
    new_data = extract_new_data('all_users.json', last_watermark)

    if not new_data:
        print("ℹ️  没有发现新数据，跳过处理")
        return

    # 3. 转换新数据
    transformed_data = transform_incremental_data(new_data)

    # 4. 加载增量数据
    load_incremental_data(transformed_data, target_file, last_watermark)

    # 5. 更新水印
    current_time = datetime.now().isoformat()
    save_current_watermark(watermark_file, current_time)

    print("=" * 50)
    print("🎉 增量ETL管道执行完成！")


if __name__ == "__main__":
    main()