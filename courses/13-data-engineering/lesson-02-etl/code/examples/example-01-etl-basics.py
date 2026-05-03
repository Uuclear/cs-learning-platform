#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETL基础示例：完整的ETL管道演示
模拟从CSV文件提取数据，进行转换处理，然后加载到目标位置
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any


def extract_data(file_path: str) -> List[Dict[str, Any]]:
    """
    提取阶段：从CSV文件读取原始数据

    Args:
        file_path: CSV文件路径

    Returns:
        包含原始数据记录的列表
    """
    print("🔄 开始提取数据...")
    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        print(f"✅ 成功提取 {len(data)} 条记录")
    except FileNotFoundError:
        print(f"❌ 文件未找到: {file_path}")
        # 创建示例数据用于演示
        data = [
            {'id': '1', 'name': '张三', 'age': '25', 'email': 'zhangsan@example.com', 'salary': '5000'},
            {'id': '2', 'name': '李四', 'age': '30', 'email': 'lisi@example.com', 'salary': '6500'},
            {'id': '3', 'name': '王五', 'age': '28', 'email': 'wangwu@example.com', 'salary': '5800'}
        ]
        print("📝 使用示例数据进行演示")

    return data


def transform_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    转换阶段：清洗和标准化数据

    转换操作包括：
    - 数据类型转换（字符串转数字）
    - 邮箱格式标准化
    - 添加处理时间戳
    - 计算薪资等级

    Args:
        raw_data: 原始数据列表

    Returns:
        转换后的标准化数据列表
    """
    print("🔄 开始转换数据...")
    transformed_data = []

    for record in raw_data:
        try:
            # 数据类型转换
            age = int(record['age'])
            salary = float(record['salary'])

            # 邮箱标准化（转为小写）
            email = record['email'].lower().strip()

            # 计算薪资等级
            if salary >= 6000:
                salary_level = '高级'
            elif salary >= 5000:
                salary_level = '中级'
            else:
                salary_level = '初级'

            # 构建转换后的记录
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

        except (ValueError, KeyError) as e:
            print(f"⚠️  跳过无效记录: {record}, 错误: {e}")
            continue

    print(f"✅ 成功转换 {len(transformed_data)} 条有效记录")
    return transformed_data


def load_data(transformed_data: List[Dict[str, Any]], output_file: str):
    """
    加载阶段：将处理后的数据保存到JSON文件

    Args:
        transformed_data: 转换后的数据列表
        output_file: 输出文件路径
    """
    print("🔄 开始加载数据...")

    try:
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(transformed_data, jsonfile, ensure_ascii=False, indent=2)
        print(f"✅ 数据成功加载到 {output_file}")
    except Exception as e:
        print(f"❌ 加载失败: {e}")


def main():
    """主函数：执行完整的ETL流程"""
    print("🚀 启动ETL管道演示")
    print("=" * 50)

    # 提取阶段
    raw_data = extract_data('employees.csv')

    # 转换阶段
    clean_data = transform_data(raw_data)

    # 加载阶段
    load_data(clean_data, 'employees_processed.json')

    print("=" * 50)
    print("🎉 ETL管道执行完成！")


if __name__ == "__main__":
    main()