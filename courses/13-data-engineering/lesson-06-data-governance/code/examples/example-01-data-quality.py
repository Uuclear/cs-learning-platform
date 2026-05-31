import json
from datetime import datetime

def check_data_completeness(data, required_fields):
    """检查数据完整性：验证必需字段是否存在且非空"""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return len(missing_fields) == 0, missing_fields

def check_data_accuracy(data, validation_rules):
    """检查数据准确性：根据业务规则验证数据"""
    errors = []
    for field, rule in validation_rules.items():
        if field in data:
            value = data[field]
            # 检查邮箱格式
            if rule == "email" and "@" not in str(value):
                errors.append(f"{field} 邮箱格式无效: {value}")
            # 检查年龄范围
            elif rule == "age" and (not isinstance(value, int) or value < 0 or value > 150):
                errors.append(f"{field} 年龄超出合理范围: {value}")
            # 检查日期格式
            elif rule == "date" and not _is_valid_date(str(value)):
                errors.append(f"{field} 日期格式无效: {value}")
    return len(errors) == 0, errors

def check_data_consistency(records, key_field, consistency_fields):
    """检查数据一致性：相同键值的记录在指定字段上应该一致"""
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

def _is_valid_date(date_string):
    """辅助函数：验证日期字符串格式"""
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

# 使用示例
if __name__ == "__main__":
    # 测试数据
    test_data = {
        "user_id": 123,
        "email": "user@example.com",
        "age": 25,
        "created_date": "2023-01-15T10:30:00Z"
    }

    # 完整性检查
    complete, missing = check_data_completeness(test_data, ["user_id", "email", "age"])
    print(f"完整性检查: {'通过' if complete else '失败'}")
    if missing:
        print(f"缺失字段: {missing}")

    # 准确性检查
    rules = {"email": "email", "age": "age", "created_date": "date"}
    accurate, errors = check_data_accuracy(test_data, rules)
    print(f"准确性检查: {'通过' if accurate else '失败'}")
    if errors:
        print(f"错误: {errors}")

    # 一致性检查
    test_records = [
        {"customer_id": "C001", "name": "张三", "region": "北京"},
        {"customer_id": "C001", "name": "张三", "region": "上海"},  # 不一致
        {"customer_id": "C002", "name": "李四", "region": "广州"}
    ]
    consistent, inconsistencies = check_data_consistency(test_records, "customer_id", ["name", "region"])
    print(f"一致性检查: {'通过' if consistent else '失败'}")
    if inconsistencies:
        print(f"不一致: {inconsistencies}")

# 预期输出:
# 完整性检查: 通过
# 准确性检查: 通过
# 一致性检查: 失败
# 不一致: ["键 C001 在字段 region 上存在不一致: {'上海', '北京'}"]