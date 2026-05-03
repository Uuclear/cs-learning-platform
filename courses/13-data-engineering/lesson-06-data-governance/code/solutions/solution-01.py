#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据质量检查解决方案

这个解决方案提供了完整的数据质量检查框架，
包括完整性、准确性、一致性和及时性四个维度的检查。
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple


def check_data_completeness(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
    """检查数据完整性：验证必需字段是否存在且非空

    Args:
        data: 要检查的数据字典
        required_fields: 必需字段列表

    Returns:
        元组：(是否完整, 缺失字段列表)
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return len(missing_fields) == 0, missing_fields


def check_data_accuracy(data: Dict[str, Any], validation_rules: Dict[str, str]) -> Tuple[bool, List[str]]:
    """检查数据准确性：根据业务规则验证数据

    Args:
        data: 要检查的数据字典
        validation_rules: 验证规则字典，键为字段名，值为规则类型

    Returns:
        元组：(是否准确, 错误信息列表)
    """
    errors = []
    for field, rule in validation_rules.items():
        if field in data:
            value = data[field]
            # 检查邮箱格式
            if rule == "email" and (not isinstance(value, str) or "@" not in value):
                errors.append(f"{field} 邮箱格式无效: {value}")
            # 检查年龄范围
            elif rule == "age" and (not isinstance(value, int) or value < 0 or value > 150):
                errors.append(f"{field} 年龄超出合理范围: {value}")
            # 检查日期格式
            elif rule == "date" and not _is_valid_date(str(value)):
                errors.append(f"{field} 日期格式无效: {value}")
            # 检查电话号码格式（简单验证）
            elif rule == "phone" and (not isinstance(value, str) or not value.replace("-", "").replace(" ", "").isdigit()):
                errors.append(f"{field} 电话号码格式无效: {value}")
            # 检查数值范围
            elif rule.startswith("range:") and isinstance(value, (int, float)):
                try:
                    min_val, max_val = map(float, rule.split(":")[1].split("-"))
                    if value < min_val or value > max_val:
                        errors.append(f"{field} 数值超出范围 [{min_val}, {max_val}]: {value}")
                except (ValueError, IndexError):
                    errors.append(f"{field} 范围规则格式错误: {rule}")
    return len(errors) == 0, errors


def check_data_consistency(records: List[Dict[str, Any]], key_field: str, consistency_fields: List[str]) -> Tuple[bool, List[str]]:
    """检查数据一致性：相同键值的记录在指定字段上应该一致

    Args:
        records: 记录列表
        key_field: 关键字段（用于分组）
        consistency_fields: 需要检查一致性的字段列表

    Returns:
        元组：(是否一致, 不一致信息列表)
    """
    grouped_data = {}
    for record in records:
        key = record.get(key_field)
        if key:
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(record)

    inconsistencies = []
    for key, group in grouped_data.items():
        if len(group) > 1:
            for field in consistency_fields:
                values = [record.get(field) for record in group if record.get(field) is not None]
                if values and len(set(values)) > 1:
                    inconsistencies.append(f"键 {key} 在字段 {field} 上存在不一致: {set(values)}")

    return len(inconsistencies) == 0, inconsistencies


def check_data_timeliness(data: Dict[str, Any], timestamp_field: str, max_age_hours: int = 24) -> Tuple[bool, str]:
    """检查数据及时性：验证数据是否在指定时间内更新

    Args:
        data: 要检查的数据字典
        timestamp_field: 时间戳字段名
        max_age_hours: 最大允许的年龄（小时）

    Returns:
        元组：(是否及时, 错误信息)
    """
    if timestamp_field not in data:
        return False, f"缺少时间戳字段: {timestamp_field}"

    try:
        timestamp_str = str(data[timestamp_field])
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        current_time = datetime.utcnow().replace(tzinfo=timestamp.tzinfo) if timestamp.tzinfo else datetime.utcnow()

        age = current_time - timestamp if current_time > timestamp else timedelta(0)
        age_hours = age.total_seconds() / 3600

        if age_hours > max_age_hours:
            return False, f"数据已过时 {age_hours:.1f} 小时，超过最大允许 {max_age_hours} 小时"
        return True, ""
    except ValueError:
        return False, f"时间戳格式无效: {data[timestamp_field]}"


def _is_valid_date(date_string: str) -> bool:
    """辅助函数：验证日期字符串格式

    Args:
        date_string: 日期字符串

    Returns:
        是否为有效日期格式
    """
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def comprehensive_data_quality_check(data_records: List[Dict[str, Any]], config: Dict[str, Any]) -> Dict[str, Any]:
    """综合数据质量检查

    Args:
        data_records: 数据记录列表
        config: 检查配置

    Returns:
        检查结果字典
    """
    results = {
        "completeness": {"passed": True, "issues": []},
        "accuracy": {"passed": True, "issues": []},
        "consistency": {"passed": True, "issues": []},
        "timeliness": {"passed": True, "issues": []},
        "overall_score": 0.0
    }

    # 完整性检查（针对第一条记录作为示例）
    if data_records:
        complete, missing = check_data_completeness(data_records[0], config.get("required_fields", []))
        results["completeness"] = {"passed": complete, "issues": missing}

    # 准确性检查（针对所有记录）
    accuracy_issues = []
    for record in data_records:
        accurate, errors = check_data_accuracy(record, config.get("validation_rules", {}))
        if not accurate:
            accuracy_issues.extend(errors)
    results["accuracy"] = {"passed": len(accuracy_issues) == 0, "issues": accuracy_issues}

    # 一致性检查
    if len(data_records) > 1 and "key_field" in config and "consistency_fields" in config:
        consistent, inconsistencies = check_data_consistency(
            data_records,
            config["key_field"],
            config["consistency_fields"]
        )
        results["consistency"] = {"passed": consistent, "issues": inconsistencies}

    # 及时性检查（针对第一条记录）
    if data_records and "timestamp_field" in config:
        timely, timeliness_issue = check_data_timeliness(
            data_records[0],
            config["timestamp_field"],
            config.get("max_age_hours", 24)
        )
        results["timeliness"] = {"passed": timely, "issues": [timeliness_issue] if not timely else []}

    # 计算总体分数
    passed_checks = sum(1 for check in results.values() if isinstance(check, dict) and check.get("passed", False))
    total_checks = 4  # completeness, accuracy, consistency, timeliness
    results["overall_score"] = round(passed_checks / total_checks * 100, 2)

    return results


def main():
    """主函数：演示数据质量检查解决方案"""
    # 测试数据
    test_records = [
        {
            "user_id": 123,
            "email": "user@example.com",
            "age": 25,
            "phone": "138-1234-5678",
            "created_date": "2023-05-02T10:30:00Z",
            "score": 85.5
        },
        {
            "user_id": 123,
            "email": "user@example.com",
            "age": 25,
            "phone": "138-1234-5678",
            "created_date": "2023-05-02T10:30:00Z",
            "score": 85.5
        },
        {
            "user_id": 456,
            "email": "invalid-email",
            "age": -5,
            "phone": "not-a-phone",
            "created_date": "invalid-date",
            "score": 150.0
        }
    ]

    # 配置检查规则
    config = {
        "required_fields": ["user_id", "email", "age"],
        "validation_rules": {
            "email": "email",
            "age": "age",
            "phone": "phone",
            "created_date": "date",
            "score": "range:0-100"
        },
        "key_field": "user_id",
        "consistency_fields": ["email", "age"],
        "timestamp_field": "created_date",
        "max_age_hours": 48
    }

    print("=== 数据质量检查解决方案演示 ===\n")

    # 执行综合检查
    results = comprehensive_data_quality_check(test_records, config)

    print(f"总体质量分数: {results['overall_score']}%")
    print()

    # 显示详细结果
    for check_type, result in results.items():
        if isinstance(result, dict) and "passed" in result:
            status = "✓ 通过" if result["passed"] else "✗ 失败"
            print(f"{check_type.capitalize()}检查: {status}")
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"   - {issue}")
            print()

    # 单独测试及时性检查（使用过时的数据）
    old_record = {"created_date": "2023-01-01T00:00:00Z"}
    timely, issue = check_data_timeliness(old_record, "created_date", max_age_hours=24)
    print(f"过时数据及时性检查: {'✓ 通过' if timely else '✗ 失败'}")
    if not timely:
        print(f"   - {issue}")


if __name__ == "__main__":
    main()