#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据质量检查示例：在ETL过程中集成数据验证
演示如何在提取、转换、加载各阶段进行数据质量检查
"""

import json
from typing import List, Dict, Any, Tuple


class DataQualityChecker:
    """数据质量检查器类"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_required_fields(self, data: List[Dict[str, Any]],
                               required_fields: List[str]) -> bool:
        """
        验证必需字段是否存在

        Args:
            data: 数据列表
            required_fields: 必需字段列表

        Returns:
            是否通过验证
        """
        print("🔍 检查必需字段...")
        valid = True

        for i, record in enumerate(data):
            for field in required_fields:
                if field not in record or record[field] is None or record[field] == '':
                    error_msg = f"记录 {i+1}: 缺少必需字段 '{field}'"
                    self.errors.append(error_msg)
                    valid = False

        return valid

    def validate_data_types(self, data: List[Dict[str, Any]],
                          type_rules: Dict[str, type]) -> bool:
        """
        验证数据类型

        Args:
            data: 数据列表
            type_rules: 字段类型规则 {字段名: 期望类型}

        Returns:
            是否通过验证
        """
        print("🔍 检查数据类型...")
        valid = True

        for i, record in enumerate(data):
            for field, expected_type in type_rules.items():
                if field in record:
                    value = record[field]
                    # 特殊处理字符串数字
                    if expected_type == int and isinstance(value, str):
                        try:
                            int(value)
                        except ValueError:
                            error_msg = f"记录 {i+1}: 字段 '{field}' 应为整数，实际值: '{value}'"
                            self.errors.append(error_msg)
                            valid = False
                    elif expected_type == float and isinstance(value, str):
                        try:
                            float(value)
                        except ValueError:
                            error_msg = f"记录 {i+1}: 字段 '{field}' 应为浮点数，实际值: '{value}'"
                            self.errors.append(error_msg)
                            valid = False
                    elif not isinstance(value, expected_type) and value is not None:
                        error_msg = f"记录 {i+1}: 字段 '{field}' 类型错误，期望 {expected_type.__name__}，实际 {type(value).__name__}"
                        self.errors.append(error_msg)
                        valid = False

        return valid

    def validate_email_format(self, data: List[Dict[str, Any]],
                             email_field: str) -> bool:
        """
        验证邮箱格式

        Args:
            data: 数据列表
            email_field: 邮箱字段名

        Returns:
            是否通过验证
        """
        print("🔍 检查邮箱格式...")
        valid = True
        import re

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        for i, record in enumerate(data):
            if email_field in record and record[email_field]:
                email = record[email_field]
                if not re.match(email_pattern, email):
                    warning_msg = f"记录 {i+1}: 邮箱格式可能无效: '{email}'"
                    self.warnings.append(warning_msg)

        return True  # 邮箱格式问题作为警告，不影响流程继续

    def check_duplicates(self, data: List[Dict[str, Any]],
                        key_fields: List[str]) -> bool:
        """
        检查重复记录

        Args:
            data: 数据列表
            key_fields: 用于判断重复的关键字段

        Returns:
            是否通过检查
        """
        print("🔍 检查重复记录...")
        valid = True

        seen_keys = set()
        for i, record in enumerate(data):
            key_tuple = tuple(record.get(field, '') for field in key_fields)
            if key_tuple in seen_keys:
                warning_msg = f"记录 {i+1}: 发现重复记录 (关键字段: {key_fields}, 值: {key_tuple})"
                self.warnings.append(warning_msg)
            else:
                seen_keys.add(key_tuple)

        return True  # 重复作为警告处理

    def get_validation_summary(self) -> Tuple[bool, List[str], List[str]]:
        """
        获取验证摘要

        Returns:
            (是否通过, 错误列表, 警告列表)
        """
        passed = len(self.errors) == 0
        return passed, self.errors, self.warnings


def extract_with_quality_check() -> List[Dict[str, Any]]:
    """
    提取阶段：包含数据质量检查的提取

    Returns:
        提取的数据列表
    """
    print("🔄 开始提取数据（带质量检查）...")

    # 模拟从源系统提取的数据（包含一些质量问题）
    raw_data = [
        {'id': '1', 'name': '张三', 'age': '25', 'email': 'zhangsan@example.com', 'salary': '5000'},
        {'id': '2', 'name': '', 'age': '30', 'email': 'lisi@invalid', 'salary': '6500'},  # 名字为空，邮箱格式问题
        {'id': '3', 'name': '王五', 'age': 'invalid', 'email': 'wangwu@example.com', 'salary': '5800'},  # 年龄类型错误
        {'id': '1', 'name': '张三', 'age': '25', 'email': 'zhangsan@example.com', 'salary': '5000'},  # 重复记录
        {'id': '4', 'name': '赵六', 'age': '35', 'email': 'zhaoliu@example.com', 'salary': ''}  # 薪资为空
    ]

    # 执行提取阶段的质量检查
    checker = DataQualityChecker()

    # 检查必需字段
    checker.validate_required_fields(raw_data, ['id', 'name'])

    # 检查数据类型（在转换前进行初步检查）
    checker.validate_data_types(raw_data, {'age': int, 'salary': float})

    # 检查邮箱格式
    checker.validate_email_format(raw_data, 'email')

    # 检查重复
    checker.check_duplicates(raw_data, ['id'])

    # 获取检查结果
    passed, errors, warnings = checker.get_validation_summary()

    print(f"📊 提取阶段质量检查结果:")
    print(f"   ✅ 通过: {passed}")
    if errors:
        print(f"   ❌ 错误 ({len(errors)}):")
        for error in errors[:3]:  # 只显示前3个错误
            print(f"      - {error}")
    if warnings:
        print(f"   ⚠️  警告 ({len(warnings)}):")
        for warning in warnings[:3]:  # 只显示前3个警告
            print(f"      - {warning}")

    return raw_data


def transform_with_quality_check(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    转换阶段：在转换过程中进行质量检查

    Args:
        raw_data: 原始数据

    Returns:
        转换后的数据
    """
    print("🔄 开始转换数据（带质量检查）...")

    transformed_data = []
    checker = DataQualityChecker()

    for record in raw_data:
        try:
            # 转换逻辑
            clean_record = {
                'employee_id': record['id'],
                'full_name': record['name'].strip() if record['name'] else '未知',
                'age': int(record['age']) if record['age'] and record['age'].isdigit() else 0,
                'email': record['email'].lower().strip() if record['email'] else '',
                'monthly_salary': float(record['salary']) if record['salary'] and record['salary'].replace('.', '').isdigit() else 0.0,
                'processed_at': '2026-05-03T12:00:00'
            }

            transformed_data.append(clean_record)

        except Exception as e:
            error_msg = f"转换失败 - 记录 {record}: {str(e)}"
            checker.errors.append(error_msg)

    # 转换后的质量检查
    checker.validate_required_fields(transformed_data, ['employee_id', 'full_name'])
    checker.validate_data_types(transformed_data, {
        'age': int,
        'monthly_salary': float
    })
    checker.validate_email_format(transformed_data, 'email')
    checker.check_duplicates(transformed_data, ['employee_id'])

    passed, errors, warnings = checker.get_validation_summary()

    print(f"📊 转换阶段质量检查结果:")
    print(f"   ✅ 通过: {passed}")
    if errors:
        print(f"   ❌ 错误 ({len(errors)}): {errors[0]}")
    if warnings:
        print(f"   ⚠️  警告 ({len(warnings)}): {warnings[0]}")

    return transformed_data


def load_with_quality_check(transformed_data: List[Dict[str, Any]]):
    """
    加载阶段：加载前的最终质量检查

    Args:
        transformed_data: 转换后的数据
    """
    print("🔄 开始最终质量检查并加载...")

    checker = DataQualityChecker()

    # 最终验证
    checker.validate_required_fields(transformed_data, ['employee_id', 'full_name', 'age'])
    checker.validate_data_types(transformed_data, {
        'age': int,
        'monthly_salary': float
    })

    passed, errors, warnings = checker.get_validation_summary()

    print(f"📊 最终质量检查结果:")
    print(f"   ✅ 通过: {passed}")

    if passed:
        # 模拟加载到目标系统
        print("✅ 数据质量合格，执行加载...")
        with open('quality_checked_data.json', 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=2)
        print("✅ 数据成功加载到 quality_checked_data.json")
    else:
        print("❌ 数据质量不合格，拒绝加载！")
        for error in errors:
            print(f"   - {error}")


def main():
    """主函数：执行带质量检查的ETL流程"""
    print("🚀 启动带数据质量检查的ETL管道")
    print("=" * 60)

    # 提取阶段（带质量检查）
    raw_data = extract_with_quality_check()
    print()

    # 转换阶段（带质量检查）
    transformed_data = transform_with_quality_check(raw_data)
    print()

    # 加载阶段（带最终质量检查）
    load_with_quality_check(transformed_data)

    print("=" * 60)
    print("🎉 带数据质量检查的ETL管道执行完成！")


if __name__ == "__main__":
    main()