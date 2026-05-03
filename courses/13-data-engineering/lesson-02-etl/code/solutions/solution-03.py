#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案03：数据质量检查实现
"""

import json
from typing import List, Dict, Any, Tuple
import re


class DataQualityChecker:
    """数据质量检查器"""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_required_fields(self, data: List[Dict[str, Any]], required_fields: List[str]) -> bool:
        """验证必需字段"""
        valid = True
        for i, record in enumerate(data):
            for field in required_fields:
                if field not in record or not record[field]:
                    self.errors.append(f"记录 {i+1}: 缺少必需字段 '{field}'")
                    valid = False
        return valid

    def validate_data_types(self, data: List[Dict[str, Any]], type_rules: Dict[str, type]) -> bool:
        """验证数据类型"""
        valid = True
        for i, record in enumerate(data):
            for field, expected_type in type_rules.items():
                if field in record and record[field]:
                    value = record[field]
                    if expected_type == int:
                        try:
                            int(value)
                        except ValueError:
                            self.errors.append(f"记录 {i+1}: 字段 '{field}' 应为整数")
                            valid = False
                    elif expected_type == float:
                        try:
                            float(value)
                        except ValueError:
                            self.errors.append(f"记录 {i+1}: 字段 '{field}' 应为数字")
                            valid = False
        return valid

    def validate_email_format(self, data: List[Dict[str, Any]], email_field: str) -> bool:
        """验证邮箱格式"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for i, record in enumerate(data):
            if email_field in record and record[email_field]:
                if not re.match(email_pattern, record[email_field]):
                    self.warnings.append(f"记录 {i+1}: 邮箱格式可能无效")
        return True

    def check_duplicates(self, data: List[Dict[str, Any]], key_fields: List[str]) -> bool:
        """检查重复记录"""
        seen_keys = set()
        for i, record in enumerate(data):
            key_tuple = tuple(record.get(field, '') for field in key_fields)
            if key_tuple in seen_keys:
                self.warnings.append(f"记录 {i+1}: 发现重复记录")
            else:
                seen_keys.add(key_tuple)
        return True

    def get_validation_summary(self) -> Tuple[bool, List[str], List[str]]:
        """获取验证摘要"""
        passed = len(self.errors) == 0
        return passed, self.errors, self.warnings


def main():
    # 模拟数据
    raw_data = [
        {'id': '1', 'name': '张三', 'age': '25', 'email': 'zhangsan@example.com'},
        {'id': '2', 'name': '', 'age': '30', 'email': 'invalid-email'},
        {'id': '3', 'name': '王五', 'age': 'invalid', 'email': 'wangwu@example.com'}
    ]

    checker = DataQualityChecker()
    checker.validate_required_fields(raw_data, ['id', 'name'])
    checker.validate_data_types(raw_data, {'age': int})
    checker.validate_email_format(raw_data, 'email')
    checker.check_duplicates(raw_data, ['id'])

    passed, errors, warnings = checker.get_validation_summary()

    if passed:
        print("✅ 数据质量检查通过")
        # 执行ETL流程
    else:
        print("❌ 数据质量检查失败:")
        for error in errors:
            print(f"   - {error}")


if __name__ == "__main__":
    main()