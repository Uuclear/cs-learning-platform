#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案02：增量加载实现
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any


def load_last_watermark(watermark_file: str) -> str:
    """加载上次处理的时间戳"""
    if os.path.exists(watermark_file):
        with open(watermark_file, 'r') as f:
            return f.read().strip()
    else:
        return (datetime.now() - timedelta(hours=24)).isoformat()


def save_current_watermark(watermark_file: str, current_time: str):
    """保存当前时间戳"""
    with open(watermark_file, 'w') as f:
        f.write(current_time)


def extract_new_data(all_data: List[Dict[str, Any]], last_watermark: str) -> List[Dict[str, Any]]:
    """提取新数据"""
    last_watermark_dt = datetime.fromisoformat(last_watermark.replace('Z', '+00:00'))
    new_records = []

    for record in all_data:
        record_time = datetime.fromisoformat(record['updated_at'].replace('Z', '+00:00'))
        if record_time > last_watermark_dt:
            new_records.append(record)

    return new_records


def transform_incremental_data(new_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """转换增量数据"""
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
    return transformed_data


def load_incremental_data(transformed_data: List[Dict[str, Any]], target_file: str):
    """增量加载数据"""
    existing_data = []
    if os.path.exists(target_file):
        with open(target_file, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []

    # 合并并去重
    combined_data = existing_data + transformed_data
    unique_data = {record['user_id']: record for record in combined_data}
    final_data = list(unique_data.values())

    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)


def main():
    watermark_file = 'watermark.txt'
    target_file = 'output.json'

    last_watermark = load_last_watermark(watermark_file)
    all_data = []  # 这里应该从实际数据源获取

    new_data = extract_new_data(all_data, last_watermark)
    if new_data:
        transformed_data = transform_incremental_data(new_data)
        load_incremental_data(transformed_data, target_file)
        save_current_watermark(watermark_file, datetime.now().isoformat())


if __name__ == "__main__":
    main()