#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案01：完整的ETL管道实现
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any


def extract_data(file_path: str) -> List[Dict[str, Any]]:
    """提取数据从CSV文件"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        # 返回空列表，让调用者处理
        return []
    return data


def transform_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """转换和清洗数据"""
    transformed_data = []

    for record in raw_data:
        try:
            age = int(record['age'])
            salary = float(record['salary'])
            email = record['email'].lower().strip()

            if salary >= 6000:
                salary_level = '高级'
            elif salary >= 5000:
                salary_level = '中级'
            else:
                salary_level = '初级'

            transformed_record = {
                'employee_id': record['id'],
                'full_name': record['name'].strip(),
                'age': age,
                'email': email,
                'monthly_salary': salary,
                'salary_level': salary_level,
                'processed_at': datetime.now().isoformat()
            }
            transformed_data.append(transformed_record)

        except (ValueError, KeyError):
            continue

    return transformed_data


def load_data(transformed_data: List[Dict[str, Any]], output_file: str):
    """加载数据到JSON文件"""
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(transformed_data, jsonfile, ensure_ascii=False, indent=2)


def main():
    raw_data = extract_data('input.csv')
    clean_data = transform_data(raw_data)
    load_data(clean_data, 'output.json')


if __name__ == "__main__":
    main()